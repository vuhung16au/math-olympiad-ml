"""
Drone System Management
Handles individual drone physics, state tracking, and movement simulation.
"""

import numpy as np
from config.drone_config import (
    TOTAL_DRONES, MAX_SPEED, ACCELERATION, DECELERATION,
    MIN_SEPARATION, POSITION_DRIFT
)


class Drone:
    """
    Represents a single drone with physics simulation.
    """
    
    def __init__(self, drone_id, initial_position=(0, 0, 0)):
        """
        Initialize a drone.
        
        Args:
            drone_id: Unique identifier for the drone
            initial_position: Starting (x, y, z) position
        """
        self.id = drone_id
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.zeros(3, dtype=float)
        self.target_position = np.array(initial_position, dtype=float)
        self.color = np.array([0, 0, 0], dtype=int)  # RGB 0-255
        self.light_on = False
        
    def set_target(self, target_position, target_color, light_on=True):
        """
        Set new target position and appearance.
        
        Args:
            target_position: Desired (x, y, z) position
            target_color: RGB tuple (0-255)
            light_on: Whether light should be on
        """
        self.target_position = np.array(target_position, dtype=float)
        self.color = np.array(target_color, dtype=int)
        self.light_on = light_on
    
    def update_physics(self, dt):
        """
        Update drone position using physics simulation.
        
        Args:
            dt: Time delta in seconds
        """
        # Calculate direction to target
        direction = self.target_position - self.position
        distance = np.linalg.norm(direction)
        
        if distance < 0.01:  # Already at target
            self.velocity = np.zeros(3)
            return
        
        # Normalize direction
        direction_normalized = direction / distance
        
        # Calculate desired velocity
        desired_speed = min(MAX_SPEED, distance / dt)
        desired_velocity = direction_normalized * desired_speed
        
        # Calculate velocity change (acceleration)
        velocity_change = desired_velocity - self.velocity
        max_velocity_change = ACCELERATION * dt
        
        if np.linalg.norm(velocity_change) > max_velocity_change:
            velocity_change = velocity_change / np.linalg.norm(velocity_change) * max_velocity_change
        
        # Update velocity
        self.velocity += velocity_change
        
        # Limit to max speed
        speed = np.linalg.norm(self.velocity)
        if speed > MAX_SPEED:
            self.velocity = self.velocity / speed * MAX_SPEED
        
        # Update position
        self.position += self.velocity * dt
        
        # Add position drift for realism
        if POSITION_DRIFT > 0:
            drift = np.random.uniform(-POSITION_DRIFT, POSITION_DRIFT, 3)
            self.position += drift
    
    def get_state(self):
        """
        Get current drone state.
        
        Returns:
            dict with position, velocity, color, light_on
        """
        return {
            'id': self.id,
            'position': self.position.copy(),
            'velocity': self.velocity.copy(),
            'color': self.color.copy(),
            'light_on': self.light_on
        }


class DroneSystem:
    """
    Manages the entire swarm of drones.
    """
    
    def __init__(self, num_drones=TOTAL_DRONES):
        """
        Initialize the drone system.
        
        Args:
            num_drones: Total number of drones to manage
        """
        self.num_drones = num_drones
        self.drones = [Drone(i, (0, 0, 0)) for i in range(num_drones)]
        self.current_time = 0.0
    
    def set_formation(self, positions, colors, lights_on=None):
        """
        Set target formation for all drones.
        
        Args:
            positions: numpy array of shape (N, 3) with target positions
            colors: numpy array of shape (N, 3) with RGB colors (0-255)
            lights_on: numpy array of shape (N,) with boolean light states
                       If None, all lights on for non-zero colors
        """
        num_active = min(len(positions), self.num_drones)
        
        if lights_on is None:
            # Default: lights on if color is not black
            lights_on = np.any(colors > 0, axis=1)
        
        # Set targets for active drones
        for i in range(num_active):
            self.drones[i].set_target(
                positions[i],
                colors[i],
                lights_on[i] if i < len(lights_on) else True
            )
        
        # Remaining drones turn off lights and stay in place
        for i in range(num_active, self.num_drones):
            self.drones[i].light_on = False
            self.drones[i].color = np.array([0, 0, 0])
    
    def update(self, dt):
        """
        Update all drones' physics.
        
        Args:
            dt: Time delta in seconds
        """
        for drone in self.drones:
            drone.update_physics(dt)
        
        self.current_time += dt
    
    def get_positions(self):
        """
        Get current positions of all drones.
        
        Returns:
            numpy array of shape (num_drones, 3)
        """
        return np.array([drone.position for drone in self.drones])
    
    def get_colors(self):
        """
        Get current colors of all drones.
        
        Returns:
            numpy array of shape (num_drones, 3) with RGB values (0-255)
        """
        return np.array([drone.color if drone.light_on else [0, 0, 0] 
                        for drone in self.drones])
    
    def get_colors_normalized(self):
        """
        Get current colors normalized to 0-1 range.
        
        Returns:
            numpy array of shape (num_drones, 3) with RGB values (0-1)
        """
        colors = self.get_colors()
        return colors / 255.0
    
    def get_all_states(self):
        """
        Get states of all drones.
        
        Returns:
            list of state dictionaries
        """
        return [drone.get_state() for drone in self.drones]
    
    def check_collisions(self):
        """
        Check for any collisions (drones within MIN_SEPARATION).
        
        Returns:
            list of tuples (drone_id1, drone_id2, distance) for colliding pairs
        """
        collisions = []
        positions = self.get_positions()
        
        for i in range(self.num_drones):
            for j in range(i + 1, self.num_drones):
                distance = np.linalg.norm(positions[i] - positions[j])
                if distance < MIN_SEPARATION:
                    collisions.append((i, j, distance))
        
        return collisions
    
    def apply_ease_curve(self, t, curve_type='ease_in_out'):
        """
        Apply easing curve to time parameter.
        
        Args:
            t: Time parameter (0-1)
            curve_type: 'ease_in_out', 'ease_in', 'ease_out', or 'linear'
        
        Returns:
            Eased time value (0-1)
        """
        if curve_type == 'linear':
            return t
        elif curve_type == 'ease_in':
            return t * t
        elif curve_type == 'ease_out':
            return 1 - (1 - t) ** 2
        elif curve_type == 'ease_in_out':
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) ** 2
        else:
            return t


def ease_in_out(t):
    """
    Smooth ease-in-ease-out curve.
    
    Args:
        t: Time parameter (0-1)
    
    Returns:
        Smoothed value (0-1)
    """
    if t < 0.5:
        return 2 * t * t
    else:
        return 1 - 2 * (1 - t) ** 2


def interpolate_positions(start_positions, end_positions, t, ease=True):
    """
    Interpolate between two sets of positions.
    
    Args:
        start_positions: numpy array of shape (N, 3)
        end_positions: numpy array of shape (N, 3)
        t: Interpolation factor (0-1)
        ease: Whether to apply easing curve
    
    Returns:
        Interpolated positions array
    """
    if ease:
        t = ease_in_out(t)
    
    return start_positions + t * (end_positions - start_positions)


def interpolate_colors(start_colors, end_colors, t, ease=True):
    """
    Interpolate between two sets of colors.
    
    Args:
        start_colors: numpy array of shape (N, 3) with RGB (0-255)
        end_colors: numpy array of shape (N, 3) with RGB (0-255)
        t: Interpolation factor (0-1)
        ease: Whether to apply easing curve
    
    Returns:
        Interpolated colors array (rounded to integers)
    """
    if ease:
        t = ease_in_out(t)
    
    interpolated = start_colors + t * (end_colors - start_colors)
    return np.round(interpolated).astype(int)


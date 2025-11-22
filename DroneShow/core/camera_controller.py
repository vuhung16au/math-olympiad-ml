"""
Camera Controller
Manages orbiting camera position and view throughout the show.
"""

import numpy as np
from config.drone_config import (
    CAMERA_FIXED, CAMERA_POSITION, CAMERA_TARGET,
    CAMERA_RADIUS, CAMERA_ORBIT_PERIOD,
    CAMERA_HEIGHT_MIN, CAMERA_HEIGHT_MAX, CAMERA_FOV, CAMERA_INITIAL_ANGLE
)


class CameraController:
    """
    Controls camera position for orbiting view of drone show.
    """
    
    def __init__(self, target=None, radius=None, orbit_period=None,
                 height_min=None, height_max=None, fov=None, initial_angle=None):
        """
        Initialize camera controller.
        
        Args:
            target: Look-at point (x, y, z) - defaults to CAMERA_TARGET
            radius: Orbit radius in meters - defaults to CAMERA_RADIUS
            orbit_period: Time for 360° rotation in seconds - defaults to CAMERA_ORBIT_PERIOD
            height_min: Minimum camera height - defaults to CAMERA_HEIGHT_MIN
            height_max: Maximum camera height - defaults to CAMERA_HEIGHT_MAX
            fov: Field of view in degrees - defaults to CAMERA_FOV
            initial_angle: Starting angle in degrees - defaults to CAMERA_INITIAL_ANGLE
        """
        self.target = np.array(target if target else CAMERA_TARGET, dtype=float)
        self.radius = radius if radius else CAMERA_RADIUS
        self.orbit_period = orbit_period if orbit_period else CAMERA_ORBIT_PERIOD
        self.height_min = height_min if height_min else CAMERA_HEIGHT_MIN
        self.height_max = height_max if height_max else CAMERA_HEIGHT_MAX
        self.fov = fov if fov else CAMERA_FOV
        self.initial_angle = initial_angle if initial_angle else CAMERA_INITIAL_ANGLE
        
        self.current_time = 0.0
    
    def get_position(self, time):
        """
        Get camera position at given time.
        
        Args:
            time: Current time in seconds
        
        Returns:
            position: (x, y, z) tuple
        """
        # Check if camera is fixed or orbiting
        if CAMERA_FIXED:
            # Fixed camera position (2D audience view)
            return CAMERA_POSITION
        
        # Orbiting camera (legacy 3D mode)
        # Calculate angle based on time (continuous orbit)
        angle_deg = self.initial_angle + (time / self.orbit_period) * 360.0
        angle_rad = np.deg2rad(angle_deg)
        
        # Calculate position on circular orbit
        x = self.target[0] + self.radius * np.cos(angle_rad)
        y = self.target[1] + self.radius * np.sin(angle_rad)
        
        # Vary height smoothly (could add more complex patterns)
        # Simple: average of min and max
        z = (self.height_min + self.height_max) / 2.0
        
        # Optional: vary height with orbit for more dynamic view
        # z = self.height_min + (self.height_max - self.height_min) * \
        #     (0.5 + 0.5 * np.sin(angle_rad))
        
        return (x, y, z)
    
    def get_view_angles(self, time):
        """
        Get camera elevation and azimuth angles at given time.
        
        Args:
            time: Current time in seconds
        
        Returns:
            elevation: Elevation angle in degrees
            azimuth: Azimuth angle in degrees
        """
        position = self.get_position(time)
        
        # Calculate direction from camera to target
        direction = self.target - np.array(position)
        
        # Calculate azimuth (horizontal angle)
        azimuth_rad = np.arctan2(direction[1], direction[0])
        azimuth_deg = np.rad2deg(azimuth_rad)
        
        # Calculate elevation (vertical angle)
        horizontal_distance = np.sqrt(direction[0]**2 + direction[1]**2)
        elevation_rad = np.arctan2(direction[2], horizontal_distance)
        elevation_deg = np.rad2deg(elevation_rad)
        
        return elevation_deg, azimuth_deg
    
    def apply_to_axes(self, ax, time):
        """
        Apply camera position and viewing angles to matplotlib 3D axes.
        
        Args:
            ax: matplotlib 3D axes
            time: Current time in seconds
        """
        position = self.get_position(time)
        elevation, azimuth = self.get_view_angles(time)
        
        # Set view
        ax.view_init(elev=elevation, azim=azimuth)
        
        # Calculate distance for consistent framing
        # Distance from camera to target
        distance = self.radius
        
        # Set limits centered on target
        # The actual limits depend on the field of view and distance
        # For simplicity, we'll use fixed limits that show the performance space
        ax.set_xlim(self.target[0] - 60, self.target[0] + 60)
        ax.set_ylim(self.target[1] - 60, self.target[1] + 60)
        ax.set_zlim(0, 30)
    
    def get_camera_info(self, time):
        """
        Get detailed camera information at given time.
        
        Args:
            time: Current time in seconds
        
        Returns:
            dict with camera information
        """
        position = self.get_position(time)
        elevation, azimuth = self.get_view_angles(time)
        
        return {
            'time': time,
            'position': position,
            'target': tuple(self.target),
            'elevation': elevation,
            'azimuth': azimuth,
            'fov': self.fov,
            'radius': self.radius
        }
    
    def get_orbit_info(self):
        """
        Get information about the camera orbit.
        
        Returns:
            dict with orbit parameters
        """
        return {
            'target': tuple(self.target),
            'radius': self.radius,
            'orbit_period': self.orbit_period,
            'angular_speed': 360.0 / self.orbit_period,  # degrees per second
            'height_range': (self.height_min, self.height_max),
            'fov': self.fov
        }


def calculate_optimal_camera_distance(formation_size, fov=60):
    """
    Calculate optimal camera distance to frame a formation.
    
    Args:
        formation_size: Maximum dimension of formation in meters
        fov: Field of view in degrees
    
    Returns:
        distance: Optimal distance in meters
    """
    # Simple calculation based on FOV
    fov_rad = np.deg2rad(fov)
    distance = (formation_size / 2.0) / np.tan(fov_rad / 2.0)
    
    # Add margin
    return distance * 1.5


def create_custom_camera_path(waypoints, durations):
    """
    Create a custom camera path through specified waypoints.
    
    Args:
        waypoints: List of (x, y, z) positions
        durations: List of durations between waypoints in seconds
    
    Returns:
        Function that takes time and returns camera position
    """
    def get_position(time):
        # Find current segment
        elapsed = 0.0
        for i, duration in enumerate(durations):
            if elapsed + duration > time:
                # Interpolate between waypoint i and i+1
                t = (time - elapsed) / duration
                # Ease-in-ease-out
                if t < 0.5:
                    t_eased = 2 * t * t
                else:
                    t_eased = 1 - 2 * (1 - t) ** 2
                
                start = np.array(waypoints[i])
                end = np.array(waypoints[i + 1])
                return tuple(start + t_eased * (end - start))
            
            elapsed += duration
        
        # Past end, return last waypoint
        return waypoints[-1]
    
    return get_position


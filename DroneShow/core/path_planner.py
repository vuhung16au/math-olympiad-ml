"""
Path Planning with Collision Avoidance
Pre-calculates drone paths and resolves conflicts using priority-based system.
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
from config.drone_config import MIN_SEPARATION, MAX_SPEED


class PathPlanner:
    """
    Plans collision-free paths for all drones.
    """
    
    def __init__(self, num_drones=1000):
        """
        Initialize path planner.
        
        Args:
            num_drones: Total number of drones
        """
        self.num_drones = num_drones
        self.paths = {}  # Will store pre-calculated paths
    
    def assign_drones_to_targets(self, start_positions, target_positions):
        """
        Assign drones to target positions minimizing total travel distance.
        Uses Hungarian algorithm for optimal assignment.
        
        Args:
            start_positions: numpy array of shape (N, 3) - current positions
            target_positions: numpy array of shape (M, 3) - target positions
        
        Returns:
            assignment: array of shape (N,) where assignment[i] is the target
                       index for drone i (-1 if no target assigned)
        """
        num_drones = len(start_positions)
        num_targets = len(target_positions)
        
        # If more targets than drones, select closest targets
        if num_targets > num_drones:
            target_positions = target_positions[:num_drones]
            num_targets = num_drones
        
        # Calculate cost matrix (Euclidean distances)
        cost_matrix = np.zeros((num_drones, num_targets))
        for i in range(num_drones):
            for j in range(num_targets):
                distance = np.linalg.norm(start_positions[i] - target_positions[j])
                cost_matrix[i, j] = distance
        
        # Solve assignment problem
        if num_targets > 0:
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            
            # Create full assignment array
            assignment = np.full(num_drones, -1, dtype=int)
            assignment[row_ind] = col_ind
        else:
            assignment = np.full(num_drones, -1, dtype=int)
        
        return assignment
    
    def generate_straight_path(self, start_pos, end_pos, duration, fps=30):
        """
        Generate straight-line path between two positions.
        
        Args:
            start_pos: Starting position (x, y, z)
            end_pos: Ending position (x, y, z)
            duration: Duration in seconds
            fps: Frames per second
        
        Returns:
            path: numpy array of shape (num_frames, 3) with positions at each frame
        """
        num_frames = int(duration * fps)
        path = np.zeros((num_frames, 3))
        
        for frame in range(num_frames):
            t = frame / max(num_frames - 1, 1)
            # Apply ease-in-ease-out
            if t < 0.5:
                t_eased = 2 * t * t
            else:
                t_eased = 1 - 2 * (1 - t) ** 2
            
            path[frame] = start_pos + t_eased * (end_pos - start_pos)
        
        return path
    
    def check_path_conflicts(self, path1, path2, time_interval=0.1, fps=30):
        """
        Check if two paths come within MIN_SEPARATION at any time.
        
        Args:
            path1: numpy array of shape (num_frames, 3)
            path2: numpy array of shape (num_frames, 3)
            time_interval: Check interval in seconds
            fps: Frames per second
        
        Returns:
            conflict: True if paths conflict, False otherwise
            min_distance: Minimum distance between paths
        """
        frames_per_check = max(1, int(time_interval * fps))
        min_distance = float('inf')
        
        num_frames = min(len(path1), len(path2))
        
        for frame in range(0, num_frames, frames_per_check):
            distance = np.linalg.norm(path1[frame] - path2[frame])
            min_distance = min(min_distance, distance)
            
            if distance < MIN_SEPARATION:
                return True, distance
        
        return False, min_distance
    
    def resolve_conflicts(self, paths, drone_priorities):
        """
        Resolve path conflicts using priority system.
        Lower priority drones are delayed if conflict detected.
        
        Args:
            paths: dict mapping drone_id -> path array
            drone_priorities: dict mapping drone_id -> priority value
                            (lower value = higher priority)
        
        Returns:
            resolved_paths: dict mapping drone_id -> adjusted path array
        """
        resolved_paths = {}
        sorted_drones = sorted(drone_priorities.keys(), key=lambda d: drone_priorities[d])
        
        for drone_id in sorted_drones:
            path = paths[drone_id]
            conflicts = []
            
            # Check against all higher-priority drones
            for other_id in sorted_drones:
                if other_id == drone_id:
                    break  # Reached current drone
                
                if other_id in resolved_paths:
                    has_conflict, min_dist = self.check_path_conflicts(
                        path, resolved_paths[other_id]
                    )
                    
                    if has_conflict:
                        conflicts.append((other_id, min_dist))
            
            # If conflicts exist, delay this drone's movement
            if conflicts:
                # Simple resolution: add delay at start
                delay_frames = 10  # 0.33 seconds at 30 fps
                delayed_path = np.vstack([
                    np.tile(path[0], (delay_frames, 1)),
                    path
                ])
                resolved_paths[drone_id] = delayed_path
            else:
                resolved_paths[drone_id] = path
        
        return resolved_paths
    
    def plan_formation_transition(self, start_positions, end_positions, 
                                  duration, fps=30):
        """
        Plan paths for transition from one formation to another.
        
        Args:
            start_positions: numpy array of shape (N, 3)
            end_positions: numpy array of shape (N, 3)
            duration: Transition duration in seconds
            fps: Frames per second
        
        Returns:
            paths: dict mapping drone_id -> path array
        """
        num_drones = len(start_positions)
        
        # Assign drones to targets
        assignment = self.assign_drones_to_targets(start_positions, end_positions)
        
        # Generate paths
        paths = {}
        for drone_id in range(num_drones):
            target_idx = assignment[drone_id]
            
            if target_idx >= 0 and target_idx < len(end_positions):
                # Drone has target
                end_pos = end_positions[target_idx]
            else:
                # Drone stays in place or moves to parking
                end_pos = start_positions[drone_id]
            
            path = self.generate_straight_path(
                start_positions[drone_id],
                end_pos,
                duration,
                fps
            )
            paths[drone_id] = path
        
        # Resolve conflicts using priority (drone ID is priority)
        priorities = {i: i for i in range(num_drones)}
        resolved_paths = self.resolve_conflicts(paths, priorities)
        
        return resolved_paths
    
    def get_position_at_time(self, drone_id, time, fps=30):
        """
        Get drone position at specific time from pre-calculated path.
        
        Args:
            drone_id: Drone identifier
            time: Time in seconds
            fps: Frames per second
        
        Returns:
            position: (x, y, z) coordinates
        """
        if drone_id not in self.paths:
            return np.array([0.0, 0.0, 0.0])
        
        path = self.paths[drone_id]
        frame = int(time * fps)
        frame = min(frame, len(path) - 1)
        
        return path[frame]


def calculate_path_distance(path):
    """
    Calculate total distance traveled along a path.
    
    Args:
        path: numpy array of shape (num_frames, 3)
    
    Returns:
        distance: Total distance in meters
    """
    if len(path) < 2:
        return 0.0
    
    distances = np.linalg.norm(np.diff(path, axis=0), axis=1)
    return np.sum(distances)


def validate_path(path, max_speed, fps=30):
    """
    Validate that path respects speed constraints.
    
    Args:
        path: numpy array of shape (num_frames, 3)
        max_speed: Maximum allowed speed in m/s
        fps: Frames per second
    
    Returns:
        valid: True if path is valid, False otherwise
        max_violation: Maximum speed violation in m/s (0 if valid)
    """
    if len(path) < 2:
        return True, 0.0
    
    # Calculate speeds between frames
    distances = np.linalg.norm(np.diff(path, axis=0), axis=1)
    dt = 1.0 / fps
    speeds = distances / dt
    
    max_speed_in_path = np.max(speeds)
    
    if max_speed_in_path > max_speed:
        return False, max_speed_in_path - max_speed
    
    return True, 0.0


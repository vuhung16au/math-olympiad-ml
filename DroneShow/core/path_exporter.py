"""
Path Export for Real-World Operations
Export drone flight paths to JSON and CSV formats for actual drone operations.
"""

import json
import csv
import numpy as np
from datetime import datetime
from config.drone_config import EXPORT_TIME_INTERVAL, MIN_SEPARATION


class PathExporter:
    """
    Exports drone paths to various formats for real-world operations.
    """
    
    def __init__(self, drone_system, fps=30):
        """
        Initialize path exporter.
        
        Args:
            drone_system: DroneSystem instance
            fps: Frames per second
        """
        self.drone_system = drone_system
        self.fps = fps
        self.recorded_states = []
        
    def record_frame(self, timestamp):
        """
        Record current state of all drones at given timestamp.
        
        Args:
            timestamp: Current time in seconds
        """
        states = self.drone_system.get_all_states()
        
        frame_data = {
            'timestamp': timestamp,
            'drones': []
        }
        
        for state in states:
            drone_data = {
                'id': state['id'],
                'x': float(state['position'][0]),
                'y': float(state['position'][1]),
                'z': float(state['position'][2]),
                'r': int(state['color'][0]),
                'g': int(state['color'][1]),
                'b': int(state['color'][2]),
                'light_on': bool(state['light_on'])
            }
            frame_data['drones'].append(drone_data)
        
        self.recorded_states.append(frame_data)
    
    def validate_paths(self):
        """
        Validate recorded paths for safety.
        
        Returns:
            dict with validation results
        """
        validation = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'collision_count': 0,
            'min_separation': float('inf')
        }
        
        # Check each frame for collisions
        for frame_idx, frame in enumerate(self.recorded_states):
            positions = np.array([[d['x'], d['y'], d['z']] 
                                 for d in frame['drones']])
            
            # Check all pairs
            num_drones = len(positions)
            for i in range(num_drones):
                for j in range(i + 1, num_drones):
                    distance = np.linalg.norm(positions[i] - positions[j])
                    validation['min_separation'] = min(
                        validation['min_separation'], distance
                    )
                    
                    if distance < MIN_SEPARATION:
                        validation['collision_count'] += 1
                        validation['errors'].append(
                            f"Frame {frame_idx} (t={frame['timestamp']:.2f}s): "
                            f"Drones {i} and {j} too close ({distance:.2f}m)"
                        )
        
        if validation['collision_count'] > 0:
            validation['valid'] = False
        
        # Check speed limits
        # (simplified check - would need more detailed implementation)
        
        return validation
    
    def export_json(self, output_path, include_metadata=True):
        """
        Export paths to JSON format.
        
        Args:
            output_path: Path to output JSON file
            include_metadata: Whether to include metadata
        """
        # Sample at specified interval
        interval_frames = int(EXPORT_TIME_INTERVAL * self.fps)
        sampled_states = self.recorded_states[::interval_frames]
        
        # Build export data structure
        export_data = {}
        
        if include_metadata:
            validation = self.validate_paths()
            
            export_data['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'total_drones': self.drone_system.num_drones,
                'duration': self.recorded_states[-1]['timestamp'] if self.recorded_states else 0.0,
                'fps': self.fps,
                'export_interval': EXPORT_TIME_INTERVAL,
                'num_frames': len(sampled_states),
                'validation': {
                    'valid': validation['valid'],
                    'min_separation': validation['min_separation'],
                    'collision_count': validation['collision_count']
                }
            }
        
        # Organize by drone
        drones_data = {}
        for frame in sampled_states:
            for drone in frame['drones']:
                drone_id = drone['id']
                if drone_id not in drones_data:
                    drones_data[drone_id] = []
                
                drones_data[drone_id].append({
                    't': frame['timestamp'],
                    'x': drone['x'],
                    'y': drone['y'],
                    'z': drone['z'],
                    'r': drone['r'],
                    'g': drone['g'],
                    'b': drone['b'],
                    'light': 1 if drone['light_on'] else 0
                })
        
        export_data['drones'] = [
            {'id': drone_id, 'path': path}
            for drone_id, path in sorted(drones_data.items())
        ]
        
        # Write to file
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Exported JSON to {output_path}")
        print(f"  Total drones: {self.drone_system.num_drones}")
        print(f"  Total frames: {len(sampled_states)}")
        print(f"  Duration: {export_data.get('metadata', {}).get('duration', 0):.1f}s")
    
    def export_csv(self, output_path):
        """
        Export paths to CSV format.
        
        Args:
            output_path: Path to output CSV file
        """
        # Sample at specified interval
        interval_frames = int(EXPORT_TIME_INTERVAL * self.fps)
        sampled_states = self.recorded_states[::interval_frames]
        
        # Write CSV
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'drone_id', 'timestamp', 'x', 'y', 'z',
                'r', 'g', 'b', 'light_on'
            ])
            
            # Data rows
            for frame in sampled_states:
                for drone in frame['drones']:
                    writer.writerow([
                        drone['id'],
                        f"{frame['timestamp']:.2f}",
                        f"{drone['x']:.3f}",
                        f"{drone['y']:.3f}",
                        f"{drone['z']:.3f}",
                        drone['r'],
                        drone['g'],
                        drone['b'],
                        1 if drone['light_on'] else 0
                    ])
        
        print(f"Exported CSV to {output_path}")
        print(f"  Total rows: {sum(len(frame['drones']) for frame in sampled_states)}")
    
    def export_all(self, base_path):
        """
        Export to both JSON and CSV formats.
        
        Args:
            base_path: Base path without extension (e.g., 'outputs/drone_show_paths')
        """
        self.export_json(f"{base_path}.json")
        self.export_csv(f"{base_path}.csv")
        
        # Also export validation report
        validation = self.validate_paths()
        with open(f"{base_path}_validation.txt", 'w') as f:
            f.write("Drone Show Path Validation Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Valid: {validation['valid']}\n")
            f.write(f"Minimum separation: {validation['min_separation']:.2f}m\n")
            f.write(f"Collision count: {validation['collision_count']}\n\n")
            
            if validation['errors']:
                f.write("Errors:\n")
                for error in validation['errors'][:10]:  # Limit to first 10
                    f.write(f"  - {error}\n")
                if len(validation['errors']) > 10:
                    f.write(f"  ... and {len(validation['errors']) - 10} more\n")
            
            if validation['warnings']:
                f.write("\nWarnings:\n")
                for warning in validation['warnings']:
                    f.write(f"  - {warning}\n")
        
        print(f"Exported validation report to {base_path}_validation.txt")


def export_paths_from_simulation(drone_system, recorded_frames, output_base_path, fps=30):
    """
    Convenience function to export paths from a simulation.
    
    Args:
        drone_system: DroneSystem instance
        recorded_frames: List of (timestamp, positions, colors) tuples
        output_base_path: Base path for output files
        fps: Frames per second
    """
    exporter = PathExporter(drone_system, fps)
    
    # Record all frames
    for timestamp, positions, colors in recorded_frames:
        # Update drone system state (temporarily)
        for i, (pos, color) in enumerate(zip(positions, colors)):
            drone_system.drones[i].position = pos
            drone_system.drones[i].color = color
            drone_system.drones[i].light_on = np.any(color > 0)
        
        exporter.record_frame(timestamp)
    
    # Export
    exporter.export_all(output_base_path)


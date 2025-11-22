"""
Drone Show Simulation
Main script to orchestrate and render the complete drone show.
"""

import os
import sys
import argparse
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

from config.drone_config import (
    TOTAL_DRONES, FPS, VIDEO_RESOLUTION, VIDEO_BITRATE,
    BACKGROUND_COLOR, SPACE_WIDTH, SPACE_HEIGHT
)
from core.drone_system import DroneSystem
from core.scene_controller import SceneController
from core.camera_controller import CameraController
from core.path_exporter import PathExporter


class DroneShowRenderer:
    """
    Renders the complete drone show animation.
    """
    
    def __init__(self, mode='testing', fps=FPS, export_paths=False):
        """
        Initialize the drone show renderer.
        
        Args:
            mode: 'testing' or 'production'
            fps: Frames per second
            export_paths: Whether to export flight paths
        """
        self.mode = mode
        self.fps = fps
        self.export_paths = export_paths
        
        # Initialize components
        print(f"Initializing drone show ({mode} mode)...")
        self.drone_system = DroneSystem(TOTAL_DRONES)
        self.scene_controller = SceneController(mode, fps)
        self.camera_controller = CameraController()
        
        if export_paths:
            self.path_exporter = PathExporter(self.drone_system, fps)
        else:
            self.path_exporter = None
        
        # Calculate total duration and frames
        self.total_duration = self.scene_controller.get_total_duration()
        self.total_frames = self.scene_controller.get_total_frames()
        
        print(f"  Total duration: {self.total_duration:.1f} seconds")
        print(f"  Total frames: {self.total_frames}")
        print(f"  FPS: {fps}")
        
        # Setup figure
        self._setup_figure()
    
    def _setup_figure(self):
        """Setup matplotlib figure and axes."""
        # Calculate figure size for 4K resolution
        width_inch = VIDEO_RESOLUTION[0] / 100
        height_inch = VIDEO_RESOLUTION[1] / 100
        
        self.fig = plt.figure(figsize=(width_inch, height_inch), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        # Set background color
        self.fig.patch.set_facecolor('black')
        self.ax.set_facecolor('black')
        
        # Remove axes
        self.ax.set_axis_off()
        
        # Set initial limits
        self.ax.set_xlim(-SPACE_WIDTH/2, SPACE_WIDTH/2)
        self.ax.set_ylim(-SPACE_WIDTH/2, SPACE_WIDTH/2)
        self.ax.set_zlim(0, SPACE_HEIGHT)
        
        # Initial scatter plot (will be updated)
        self.scatter = self.ax.scatter([], [], [], s=10, c=[], alpha=0.9)
    
    def update_frame(self, frame):
        """
        Update animation for given frame.
        
        Args:
            frame: Frame number
        
        Returns:
            Modified artists
        """
        # Calculate current time
        time = frame / self.fps
        
        # Get formation at this time
        positions, colors = self.scene_controller.get_formation_at_time(time)
        
        # Update drone system targets
        self.drone_system.set_formation(positions, colors)
        
        # Simulate physics (small time step)
        dt = 1.0 / self.fps
        self.drone_system.update(dt)
        
        # Get current positions and colors
        current_positions = self.drone_system.get_positions()
        current_colors = self.drone_system.get_colors_normalized()
        
        # Update scatter plot
        self.scatter._offsets3d = (
            current_positions[:, 0],
            current_positions[:, 1],
            current_positions[:, 2]
        )
        self.scatter.set_color(current_colors)
        
        # Update camera
        self.camera_controller.apply_to_axes(self.ax, time)
        
        # Record for path export if enabled
        if self.path_exporter:
            self.path_exporter.record_frame(time)
        
        return self.scatter,
    
    def render(self, output_path='outputs/drone_show.mp4'):
        """
        Render the complete animation to video.
        
        Args:
            output_path: Path to save the video
        """
        print(f"\nRendering drone show to {output_path}...")
        print("This may take several minutes...\n")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create progress bar with proper configuration
        if tqdm:
            # Configure tqdm to stay on one line
            pbar = tqdm(
                total=self.total_frames,
                desc="Rendering",
                unit="frame",
                dynamic_ncols=True,
                leave=True,
                position=0,
                file=None  # Use default (sys.stderr)
            )
            
            # Wrap update function
            original_update = self.update_frame
            def update_with_progress(frame):
                result = original_update(frame)
                pbar.update(1)
                return result
            
            update_func = update_with_progress
        else:
            update_func = self.update_frame
        
        # Create animation
        anim = FuncAnimation(
            self.fig,
            update_func,
            frames=self.total_frames,
            interval=1000/self.fps,
            blit=False
        )
        
        # Save animation with minimal verbosity
        writer = FFMpegWriter(
            fps=self.fps,
            bitrate=VIDEO_BITRATE,
            metadata={'title': 'Drone Show Simulation'}
        )
        
        # Suppress matplotlib logging during save
        matplotlib_logger = logging.getLogger('matplotlib')
        animation_logger = logging.getLogger('matplotlib.animation')
        original_mpl_level = matplotlib_logger.level
        original_anim_level = animation_logger.level
        matplotlib_logger.setLevel(logging.WARNING)
        animation_logger.setLevel(logging.WARNING)
        
        try:
            anim.save(output_path, writer=writer)
        finally:
            matplotlib_logger.setLevel(original_mpl_level)
            animation_logger.setLevel(original_anim_level)
        
        if tqdm:
            pbar.close()
        
        print(f"\n✓ Animation saved to {output_path}")
        
        # Export paths if enabled
        if self.path_exporter:
            print("\nExporting flight paths...")
            base_path = output_path.replace('.mp4', '_paths')
            self.path_exporter.export_all(base_path)
        
        plt.close(self.fig)
    
    def get_scene_info(self):
        """Get information about all scenes."""
        return self.scene_controller.get_scene_info()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate drone show simulation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick testing mode (16 seconds)
  python drone_show.py
  
  # Production mode (120 seconds)
  python drone_show.py --mode production
  
  # Export flight paths
  python drone_show.py --export-paths
  
  # Custom output path
  python drone_show.py --output outputs/my_show.mp4
  
  # Full production with path export
  python drone_show.py --mode production --export-paths --output outputs/drone_show_full.mp4
"""
    )
    
    parser.add_argument(
        '--mode', '-m',
        choices=['testing', 'production'],
        default='testing',
        help='Simulation mode: testing (16s, 2s per scene) or production (120s, 15s per scene)'
    )
    
    parser.add_argument(
        '--fps',
        type=int,
        default=FPS,
        help=f'Frames per second (default: {FPS})'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='outputs/drone_show.mp4',
        help='Output video file path (default: outputs/drone_show.mp4)'
    )
    
    parser.add_argument(
        '--export-paths',
        action='store_true',
        help='Export flight paths to JSON and CSV for real-world operations'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show scene information and exit (no rendering)'
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 70)
    print("DRONE SHOW SIMULATION")
    print("=" * 70)
    print(f"Mode: {args.mode}")
    print(f"FPS: {args.fps}")
    print(f"Output: {args.output}")
    print(f"Export paths: {args.export_paths}")
    print("=" * 70)
    
    # Create renderer
    try:
        renderer = DroneShowRenderer(
            mode=args.mode,
            fps=args.fps,
            export_paths=args.export_paths
        )
        
        # Show scene info if requested
        if args.info:
            print("\nScene Information:")
            print("-" * 70)
            for scene in renderer.get_scene_info():
                print(f"  {scene['name']:20s} | "
                      f"{scene['start_time']:6.1f}s - {scene['end_time']:6.1f}s | "
                      f"Duration: {scene['duration']:5.1f}s")
            print("-" * 70)
            return 0
        
        # Render
        renderer.render(args.output)
        
        print("\n" + "=" * 70)
        print("✓ DRONE SHOW COMPLETE")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())


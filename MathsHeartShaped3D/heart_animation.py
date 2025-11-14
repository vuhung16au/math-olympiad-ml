"""
3D Heart Animation Script
Generates a rotating 3D parametric heart shape and saves it as an MP4 video.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from mpl_toolkits.mplot3d import Axes3D
import argparse
import os


def generate_heart_points(u_points=200, v_points=200):
    """
    Generate 3D coordinates for the parametric heart shape.
    
    Parameters:
    - u_points: Number of points in the u parameter
    - v_points: Number of points in the v parameter
    
    Returns:
    - x, y, z: Arrays of 3D coordinates
    - colors: Color values for the gradient
    """
    # Create parameter grids
    u = np.linspace(0, np.pi, u_points)
    v = np.linspace(0, 2 * np.pi, v_points)
    u_grid, v_grid = np.meshgrid(u, v)
    
    # Flatten for scatter plot
    u_flat = u_grid.flatten()
    v_flat = v_grid.flatten()
    
    # Parametric equations for the 3D heart
    x = np.sin(u_flat) * (15 * np.sin(v_flat) - 4 * np.sin(3 * v_flat))
    y = 8 * np.cos(u_flat)
    z = np.sin(u_flat) * (15 * np.cos(v_flat) - 5 * np.cos(2 * v_flat) - 
                          2 * np.cos(3 * v_flat) - np.cos(4 * v_flat))
    
    # Use z values for color gradient
    colors = z
    
    return x, y, z, colors


def setup_figure(resolution='medium', dpi=100):
    """
    Set up the matplotlib figure and 3D axes.
    
    Parameters:
    - resolution: 'small', 'medium', or 'large'
    - dpi: Dots per inch for the figure
    
    Returns:
    - fig, ax: Matplotlib figure and axes objects
    """
    # Define resolution settings
    resolutions = {
        'small': (640, 480),
        'medium': (1280, 720),
        'large': (1920, 1080)
    }
    
    width, height = resolutions.get(resolution, resolutions['medium'])
    figsize = (width / dpi, height / dpi)
    
    # Create figure with black background
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Set initial view angle
    ax.view_init(elev=20, azim=45)
    
    # Hide axes, grid, and panes
    ax.axis('off')
    ax.grid(False)
    
    # Make panes transparent/black
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')
    
    return fig, ax


def create_animation(resolution='medium', dpi=100, output_path='outputs/heart_animation.mp4'):
    """
    Create and save the 3D heart rotation animation.
    
    Parameters:
    - resolution: 'small', 'medium', or 'large'
    - dpi: Dots per inch for the figure
    - output_path: Path to save the output video
    """
    print(f"Generating heart shape with 40,000 points...")
    x_original, y_original, z_original, colors = generate_heart_points()
    
    print(f"Setting up figure with resolution: {resolution}, DPI: {dpi}")
    fig, ax = setup_figure(resolution, dpi)
    
    # Initial scatter plot
    scatter = ax.scatter(x_original, y_original, z_original, 
                        c=colors, cmap='magma', s=1, alpha=0.8)
    
    # Set axis limits to keep the heart centered
    max_range = 20
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Total frames for 360-degree rotation over 30 seconds at 30 fps
    total_frames = 900
    
    def update(frame):
        """
        Update function for animation - rotates the heart around the y-axis.
        
        Parameters:
        - frame: Current frame number (0 to 899)
        """
        # Calculate rotation angle in degrees and convert to radians
        alpha_deg = frame * 360 / total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        # Apply 3D rotation matrix around y-axis
        x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
        y_rotated = y_original  # y remains unchanged
        z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
        
        # Update scatter plot data
        scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Print progress every 30 frames (every second)
        if frame % 30 == 0:
            progress = (frame / total_frames) * 100
            print(f"Progress: {progress:.1f}% ({frame}/{total_frames} frames)")
        
        return scatter,
    
    print(f"Creating animation with {total_frames} frames (30 seconds at 30 fps)...")
    print("This may take several minutes depending on your system...")
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=total_frames, 
                        interval=1000/30, blit=False)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save animation
    print(f"Saving animation to {output_path}...")
    writer = FFMpegWriter(fps=30, bitrate=5000)
    anim.save(output_path, writer=writer)
    
    print(f"✓ Animation successfully saved to {output_path}")
    plt.close(fig)


def main():
    """
    Main function to parse arguments and create the animation.
    """
    parser = argparse.ArgumentParser(
        description='Generate a 3D rotating heart animation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Resolution options:
  small   - 640x480
  medium  - 1280x720 (default)
  large   - 1920x1080

Examples:
  python heart_animation.py
  python heart_animation.py --resolution large
  python heart_animation.py --resolution small --dpi 150
        """
    )
    
    parser.add_argument(
        '--resolution', '-r',
        choices=['small', 'medium', 'large'],
        default='medium',
        help='Output video resolution (default: medium)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=100,
        help='DPI setting for rendering quality (default: 100)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='outputs/heart_animation.mp4',
        help='Output file path (default: outputs/heart_animation.mp4)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("3D Heart Animation Generator")
    print("=" * 60)
    print(f"Resolution: {args.resolution}")
    print(f"DPI: {args.dpi}")
    print(f"Output: {args.output}")
    print("=" * 60)
    
    try:
        create_animation(
            resolution=args.resolution,
            dpi=args.dpi,
            output_path=args.output
        )
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

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


def generate_heart_points(u_points=200, v_points=200, density='high'):
    """
    Generate 3D coordinates for the parametric heart shape.
    
    Parameters:
    - u_points: Number of points in the u parameter
    - v_points: Number of points in the v parameter
    - density: Point density level ('low', 'medium', 'high')
    
    Returns:
    - x, y, z: Arrays of 3D coordinates
    - colors: Color values for the gradient
    """
    # Adjust point count based on density
    density_multipliers = {
        'lower': 0.35,   # 70x70 = 4,900 points (~5,000)
        'low': 0.5,      # 100x100 = 10,000 points
        'medium': 0.75,  # 150x150 = 22,500 points
        'high': 1.0      # 200x200 = 40,000 points
    }
    multiplier = density_multipliers.get(density, 1.0)
    u_points = int(u_points * multiplier)
    v_points = int(v_points * multiplier)
    # Create parameter grids
    u = np.linspace(0, np.pi, u_points)
    v = np.linspace(0, 2 * np.pi, v_points)
    u_grid, v_grid = np.meshgrid(u, v)
    
    # Flatten for scatter plot
    u_flat = u_grid.flatten()
    v_flat = v_grid.flatten()
    
    # Parametric equations for the 3D heart
    x = np.sin(u_flat) * (15.16 * np.sin(v_flat) - 3.59 * np.sin(2.99 * v_flat))
    y = -7.9911 * np.cos(u_flat)  # Negative to flip vertically (point down)
    z = np.sin(u_flat) * (15.16 * np.cos(v_flat) - 5.11 * np.cos(2.12 * v_flat) - 
                          2 * np.cos(3.11 * v_flat) - np.cos(v_flat))
    
    # Use z values for color gradient
    colors = z
    
    return x, y, z, colors


def setup_figure(resolution='medium', dpi=100, show_axes=True, show_formulas=True):
    """
    Set up the matplotlib figure and 3D axes.
    
    Parameters:
    - resolution: 'small', 'medium', or 'large'
    - dpi: Dots per inch for the figure
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    
    Returns:
    - fig, ax: Matplotlib figure and axes objects
    """
    # Define resolution settings
    resolutions = {
        'small': (640, 480),
        'medium': (1280, 720),
        'large': (1920, 1080),
        '4k': (3840, 2160)
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
    
    # Add coordinate axes if requested
    if show_axes:
        max_range = 20
        # X-axis (red)
        ax.plot([-max_range, max_range], [0, 0], [0, 0], 'r-', linewidth=1.5, alpha=0.6)
        # Y-axis (green)
        ax.plot([0, 0], [-max_range, max_range], [0, 0], 'g-', linewidth=1.5, alpha=0.6)
        # Z-axis (blue)
        ax.plot([0, 0], [0, 0], [-max_range, max_range], 'b-', linewidth=1.5, alpha=0.6)
    
    # Add formulas text if requested
    if show_formulas:
        formula_text = (
            r'$x = \sin(u) \cdot (15.16\sin(v) - 3.59\sin(2.99v))$' + '\n'
            r'$y = 7.9911\cos(u)$' + '\n'
            r'$z = \sin(u) \cdot (15.16\cos(v) - 5.11\cos(2.12v) - 2\cos(3.11v) - \cos(v))$' + '\n'
            r'$u \in [0, \pi], \quad v \in [0, 2\pi]$'
        )
        fig.text(0.02, 0.98, formula_text, 
                transform=fig.transFigure,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='left',
                color='white',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.7, edgecolor='white', linewidth=0.5))
    
    return fig, ax


def create_animation(resolution='medium', dpi=100, density='high', effect='A',
                    show_axes=False, show_formulas=False, fps=30, bitrate=5000, output_path='outputs/heart_animation.mp4'):
    """
    Create and save the 3D heart rotation animation.
    
    Parameters:
    - resolution: 'small', 'medium', 'large', or '4k'
    - dpi: Dots per inch for the figure
    - density: Point density ('lower', 'low', 'medium', 'high')
    - effect: Animation effect ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2')
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    - fps: Frames per second for output video (default: 30)
    - bitrate: Video bitrate in kbps (default: 5000)
    - output_path: Path to save the output video
    """
    # Calculate actual point count
    point_counts = {'lower': '~5,000', 'low': '10,000', 'medium': '22,500', 'high': '40,000'}
    effect_names = {
        'A': 'Multi-axis rotation (Y + X wobble)',
        'B': 'Dynamic camera orbit',
        'C': 'Combined (rotation + camera + zoom)',
        'D': 'Custom (Y rotation + elevation sweep + zoom)',
        'E': 'Heartbeat Pulse (rotation + rhythmic scaling)',
        'F': 'Spiral Ascent (rotation + spiral camera + zoom out)',
        'G': 'Figure-8 Dance (rotation + figure-8 camera path)',
        'G1': 'Heart Journey (camera through heart + moon orbit - 90s)',
        'G2': 'Epic Heart Story (fade in/out + formulas + through heart + orbit - 137s)'
    }
    print(f"Generating heart shape with {point_counts.get(density, '40,000')} points (density: {density})...")
    print(f"Effect: {effect} - {effect_names.get(effect, 'Simple Y-axis rotation')}")
    x_original, y_original, z_original, colors = generate_heart_points(density=density)
    
    print(f"Setting up figure with resolution: {resolution}, DPI: {dpi}")
    fig, ax = setup_figure(resolution, dpi, show_axes, show_formulas)
    
    # Initial scatter plot
    scatter = ax.scatter(x_original, y_original, z_original, 
                        c=colors, cmap='magma', s=1, alpha=0.8)
    
    # Set axis limits to keep the heart centered with 16:9 aspect ratio
    max_range = 20
    ax.set_xlim([-max_range * 1.78, max_range * 1.78])  # 16:9 widescreen
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Total frames - adjust for longer effects
    if effect == 'G1':
        total_frames = 2700  # 90 seconds at 30 fps for G1
        duration_text = "90 seconds"
    elif effect == 'G2':
        total_frames = 4110  # 137 seconds at 30 fps for G2
        duration_text = "137 seconds"
    else:
        total_frames = 900   # 30 seconds at 30 fps for other effects
        duration_text = "30 seconds"
    
    def update(frame):
        """
        Update function for animation - applies different effects based on mode.
        
        Parameters:
        - frame: Current frame number (0 to 899)
        """
        # Calculate normalized time (0 to 1)
        t = frame / total_frames
        
        # Effect A: Multi-axis rotation (Y-axis + X-axis wobble)
        if effect == 'A':
            # Primary rotation around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            # Add gentle X-axis wobble (15-degree amplitude)
            beta_deg = 15 * np.sin(2 * np.pi * t)
            beta_rad = np.deg2rad(beta_deg)
            
            # Rotate around Y-axis first
            x_temp = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_temp = y_original
            z_temp = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Then rotate around X-axis for wobble
            x_rotated = x_temp
            y_rotated = y_temp * np.cos(beta_rad) - z_temp * np.sin(beta_rad)
            z_rotated = y_temp * np.sin(beta_rad) + z_temp * np.cos(beta_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Effect B: Dynamic camera orbit (heart stays stationary)
        elif effect == 'B':
            # Heart doesn't rotate
            scatter._offsets3d = (x_original, y_original, z_original)
            
            # Camera orbits around the heart
            azimuth = 45 + 360 * t
            elevation = 20 + 20 * np.sin(2 * np.pi * t)  # Elevation oscillates
            ax.view_init(elev=elevation, azim=azimuth)
        
        # Effect C: Combined (rotating heart + orbiting camera + zoom)
        elif effect == 'C':
            # Rotate heart around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Camera orbits slower (180 degrees total)
            azimuth = 45 + 180 * t
            elevation = 20 + 15 * np.sin(np.pi * t)
            ax.view_init(elev=elevation, azim=azimuth)
            
            # Zoom effect: zoom in first half, zoom out second half
            if t < 0.5:
                zoom_factor = 20 - 5 * (t * 2)  # Zoom in from 20 to 15
            else:
                zoom_factor = 15 + 5 * ((t - 0.5) * 2)  # Zoom out from 15 to 20
            
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect D: Custom (Y rotation + elevation sweep + zoom pulse)
        elif effect == 'D':
            # Rotate around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Smooth elevation sweep from bottom to top and back
            elevation = 20 + 40 * np.sin(np.pi * t)
            ax.view_init(elev=elevation, azim=45)
            
            # Subtle zoom pulse
            zoom_factor = 20 + 3 * np.sin(4 * np.pi * t)
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect E: Heartbeat Pulse (rotation + rhythmic scaling)
        elif effect == 'E':
            # Rotate around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_temp = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_temp = y_original
            z_temp = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Heartbeat pulse: double beat pattern (lub-dub)
            # Create a heartbeat rhythm with two pulses per cycle
            heartbeat_freq = 2  # 2 beats per rotation
            pulse1 = np.sin(2 * np.pi * heartbeat_freq * t) ** 2
            pulse2 = np.sin(2 * np.pi * heartbeat_freq * t + np.pi/3) ** 2
            heartbeat = 1.0 + 0.15 * (pulse1 + 0.5 * pulse2)  # Scale between 1.0 and 1.15
            
            # Apply pulsating scale
            x_rotated = x_temp * heartbeat
            y_rotated = y_temp * heartbeat
            z_rotated = z_temp * heartbeat
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Gentle camera wobble synchronized with heartbeat
            elevation = 20 + 5 * np.sin(2 * np.pi * heartbeat_freq * t)
            ax.view_init(elev=elevation, azim=45)
        
        # Effect F: Spiral Ascent (rotation + spiral camera + zoom out)
        elif effect == 'F':
            # Rotate heart around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Camera spirals upward while orbiting
            azimuth = 45 + 720 * t  # Two full rotations
            elevation = -10 + 70 * t  # Rises from -10 to 60 degrees
            ax.view_init(elev=elevation, azim=azimuth)
            
            # Gradual zoom out as camera ascends
            zoom_factor = 20 + 15 * t  # Zoom from 20 to 35
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect G: Figure-8 Dance (rotation + figure-8 camera path)
        elif effect == 'G':
            # Rotate heart around Y-axis
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Camera follows a figure-8 (lemniscate) path
            # Parametric equations for figure-8: x = sin(t), y = sin(t)*cos(t)
            azimuth_offset = 60 * np.sin(2 * np.pi * t)  # Horizontal figure-8 component
            elevation_offset = 30 * np.sin(4 * np.pi * t)  # Vertical figure-8 component (double frequency)
            
            azimuth = 45 + azimuth_offset + 180 * t  # Also slowly rotate around
            elevation = 20 + elevation_offset
            
            ax.view_init(elev=elevation, azim=azimuth)
            
            # Subtle zoom synchronized with figure-8 motion
            zoom_factor = 20 + 4 * np.sin(2 * np.pi * t)
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect G1: Heart Journey (camera zooms through heart, then orbits back)
        elif effect == 'G1':
            # Heart rotates slowly throughout (180 degrees over 90 seconds)
            alpha_deg = frame * 180 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            # Phase 1 (0-0.22): Rapid zoom approach through heart center (0-20 seconds)
            if t < 0.22:
                phase_t = t / 0.22
                # Zoom from far (150) to through center (-10), accelerating
                zoom_factor = 150 - 160 * (phase_t ** 2)
                # Slight elevation change for drama
                elevation = 10 + 10 * np.sin(np.pi * phase_t)
                azimuth = 45
                
            # Phase 2 (0.22-0.33): Exit and turnaround behind heart (20-30 seconds)
            elif t < 0.33:
                phase_t = (t - 0.22) / 0.11
                # Continue through to behind (-10 to 40)
                zoom_factor = -10 + 50 * phase_t
                elevation = 20
                # Swing around to opposite side (180 degrees)
                azimuth = 45 + 180 * phase_t
                
            # Phase 3 (0.33-1.0): Orbital return like moon (30-90 seconds, 2 complete orbits)
            else:
                phase_t = (t - 0.33) / 0.67
                # Gradually get closer (40 to 25)
                zoom_factor = 40 - 15 * phase_t
                # Elevation oscillates like orbital path (2 cycles)
                elevation = 20 + 25 * np.sin(2 * np.pi * 2 * phase_t)
                # 2 complete orbits (720 degrees)
                azimuth = 225 + 720 * phase_t
            
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect G2: Epic Heart Story (137 seconds total - 4110 frames)
        elif effect == 'G2':
            # Convert frame to seconds for easier calculation
            current_second = frame / 30.0
            
            # Heart rotates throughout entire animation (slower - 270 degrees total)
            alpha_deg = frame * 270 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Default alpha for heart points
            point_alpha = 0.8
            
            # Phase 1 (0-1s): Fade in from black
            if current_second < 1.0:
                point_alpha = current_second  # 0 to 1
                zoom_factor = 12  # Changed from 25 to 12 (heart 2x bigger)
                elevation = 20
                azimuth = 45
                
            # Phase 2 (1-3s): Gradually show heart with G1 starting position
            elif current_second < 3.0:
                phase_t = (current_second - 1.0) / 2.0
                point_alpha = 0.8
                zoom_factor = 80 - 68 * phase_t  # 80 to 12 (closer for larger heart)
                elevation = 10 + 10 * phase_t  # 10 to 20
                azimuth = 45
                
            # Phase 3 (3-60s): Run G1 effect (first 57 seconds of it - condensed)
            elif current_second < 60.0:
                phase_t = (current_second - 3.0) / 57.0  # Normalize to 0-1
                point_alpha = 0.8
                
                # Condensed G1: zoom through, turn, and start orbit
                if phase_t < 0.35:  # 0-20s: Zoom through
                    sub_t = phase_t / 0.35
                    zoom_factor = 12 - 22 * (sub_t ** 2)  # 12 to -10 (through heart, larger)
                    elevation = 20 + 5 * np.sin(np.pi * sub_t)
                    azimuth = 45
                elif phase_t < 0.53:  # 20-30s: Exit and turn
                    sub_t = (phase_t - 0.35) / 0.18
                    zoom_factor = -10 + 22 * sub_t  # -10 to 12 (adjusted)
                    elevation = 20
                    azimuth = 45 + 180 * sub_t
                else:  # 30-60s: Start orbital motion
                    sub_t = (phase_t - 0.53) / 0.47
                    zoom_factor = 12 - 2 * sub_t  # 12 to 10 (closer orbit)
                    elevation = 20 + 20 * np.sin(2 * np.pi * sub_t)
                    azimuth = 225 + 360 * sub_t
                    
            # Phase 4 (60-62s): Fade out heart
            elif current_second < 62.0:
                phase_t = (current_second - 60.0) / 2.0
                point_alpha = 0.8 * (1.0 - phase_t)  # 0.8 to 0
                zoom_factor = 10  # Changed from 20 to 10
                elevation = 20
                azimuth = 225 + 360 * 0.53
                
            # Phase 5 (62-64s): Black screen with formulas (heart invisible)
            elif current_second < 64.0:
                point_alpha = 0.0  # Heart invisible
                zoom_factor = 10  # Changed from 20 to 10
                elevation = 20
                azimuth = 45
                # Formula display handled by setup_figure, just keep heart hidden
                
            # Phase 6 (64-66s): Fade formulas out (keep heart hidden, formulas handled by matplotlib text alpha)
            elif current_second < 66.0:
                point_alpha = 0.0  # Heart still invisible
                zoom_factor = 10  # Changed from 20 to 10
                elevation = 20
                azimuth = 45
                
            # Phase 7 (66-68s): Fade heart back in at G1 starting position
            elif current_second < 68.0:
                phase_t = (current_second - 66.0) / 2.0
                point_alpha = 0.8 * phase_t  # 0 to 0.8
                zoom_factor = 30  # Changed from 50 to 30 (closer start)
                elevation = 15
                azimuth = 45
                
            # Phase 8 (68-90s): Zoom through heart (accelerated)
            elif current_second < 90.0:
                phase_t = (current_second - 68.0) / 22.0
                point_alpha = 0.8
                zoom_factor = 30 - 50 * (phase_t ** 1.5)  # 30 to -20 (adjusted range)
                elevation = 15 + 15 * np.sin(np.pi * phase_t)
                azimuth = 45 + 90 * phase_t
                
            # Phase 9 (90-92s): Exit and show heart from behind
            elif current_second < 92.0:
                phase_t = (current_second - 90.0) / 2.0
                point_alpha = 0.8
                zoom_factor = -20 + 35 * phase_t  # -20 to 15 (closer)
                elevation = 30
                azimuth = 135 + 90 * phase_t  # Complete the turn
                
            # Phase 10 (92-102s): Slow zoom out, heart gets smaller
            elif current_second < 102.0:
                phase_t = (current_second - 92.0) / 10.0
                point_alpha = 0.8
                zoom_factor = 15 + 50 * phase_t  # 15 to 65 (not as far)
                elevation = 30 - 10 * phase_t  # Slowly descend
                azimuth = 225 + 180 * phase_t
                
            # Phase 11 (102-122s): Zoom back in dramatically
            elif current_second < 122.0:
                phase_t = (current_second - 102.0) / 20.0
                point_alpha = 0.8
                # Dramatic zoom: 65 down to 10 (very close)
                zoom_factor = 65 - 55 * (phase_t ** 2)  # Accelerating zoom in
                elevation = 20 + 25 * np.sin(np.pi * phase_t)  # Dramatic arc
                azimuth = 405 + 270 * phase_t  # Continue orbit
                
            # Phase 12 (122-132s): Moon orbit around heart
            elif current_second < 132.0:
                phase_t = (current_second - 122.0) / 10.0
                point_alpha = 0.8
                zoom_factor = 10 + 4 * np.sin(2 * np.pi * phase_t)  # Closer orbit (10±4)
                elevation = 25 + 15 * np.sin(2 * np.pi * 2 * phase_t)  # 2 oscillations
                azimuth = 675 + 720 * phase_t  # 2 complete orbits
                
            # Phase 13 (132-137s): Quick zoom out and fade to black
            elif current_second < 137.0:
                phase_t = (current_second - 132.0) / 5.0
                point_alpha = 0.8 * (1.0 - phase_t)  # Fade out: 0.8 to 0
                zoom_factor = 10 + 60 * (phase_t ** 2)  # 10 to 70 (less dramatic)
                elevation = 25 - 25 * phase_t  # Return to neutral
                azimuth = 1395 + 180 * phase_t
            
            else:
                # Fallback (shouldn't reach here)
                point_alpha = 0.0
                zoom_factor = 10  # Changed from 20 to 10
                elevation = 20
                azimuth = 45
            
            # Apply alpha to scatter plot
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor * 1.78, zoom_factor * 1.78])  # 16:9
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        else:
            # Default: simple Y-axis rotation (original behavior)
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Print progress every 30 frames (every second)
        if frame % 30 == 0:
            progress = (frame / total_frames) * 100
            print(f"Progress: {progress:.1f}% ({frame}/{total_frames} frames)")
        
        return scatter,
    
    print(f"Creating animation with {total_frames} frames ({duration_text} at {fps} fps)...")
    print("This may take several minutes depending on your system...")
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=total_frames, 
                        interval=1000/30, blit=False)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save animation
    print(f"Saving animation to {output_path}...")
    writer = FFMpegWriter(fps=fps, bitrate=bitrate)
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
  small   - 640x480 (SD)
  medium  - 1280x720 (HD, default)
  large   - 1920x1080 (Full HD)
  4k      - 3840x2160 (4K Ultra HD)

Density options:
  lower   - ~5,000 points (fastest)
  low     - 10,000 points (default)
  medium  - 22,500 points
  high    - 40,000 points (best quality)

Effect options:
  A - Multi-axis rotation: Heart spins on Y-axis with gentle X-axis wobble
  B - Dynamic camera orbit: Camera circles around stationary heart with elevation changes
  C - Combined: Rotating heart + orbiting camera + zoom in/out effect
  D - Custom: Y-axis rotation + elevation sweep + subtle zoom pulse
  E - Heartbeat Pulse: Heart rotates and pulses rhythmically like a beating heart
  F - Spiral Ascent: Camera spirals upward while heart rotates, zooming out dramatically
  G - Figure-8 Dance: Camera follows infinity symbol path while heart rotates
  G1 - Heart Journey: Camera zooms through heart center, exits behind, then orbits back like moon (90 seconds, fast-paced)
  G2 - Epic Heart Story: Cinematic sequence with fade in/out, formula display, dramatic zooms through heart, 
       distant zoom out, dramatic zoom back in, moon orbit, and fade to black (137 seconds, epic storytelling)

Examples:
  python heart_animation.py
  python heart_animation.py --resolution large --effect C
  python heart_animation.py --density lower --effect E
  python heart_animation.py --resolution medium --effect F
  python heart_animation.py --resolution small --dpi 150 --effect G
  python heart_animation.py --density low --effect G1 --output outputs/heart_journey.mp4
  python heart_animation.py --density lower --effect G2 --output outputs/epic_heart_story.mp4
  python heart_animation.py --resolution 4k --bitrate 20000 --effect G2 --output outputs/epic_4k.mp4
        """
    )
    
    parser.add_argument(
        '--resolution', '-r',
        choices=['small', 'medium', 'large', '4k'],
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
        '--density', '-d',
        choices=['lower', 'low', 'medium', 'high'],
        default='low',
        help='Point density: lower (~5K), low (10K), medium (22.5K), high (40K) (default: low)'
    )
    
    parser.add_argument(
        '--effect', '-e',
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2'],
        default='A',
        help='Animation effect: A (multi-axis), B (camera orbit), C (combined), D (custom), E (heartbeat), F (spiral), G (figure-8), G1 (journey 90s), G2 (epic story 137s) (default: A)'
    )
    
    parser.add_argument(
        '--axes',
        action='store_true',
        help='Show coordinate axes lines'
    )
    
    parser.add_argument(
        '--formulas',
        action='store_true',
        help='Show parametric formulas text'
    )
    
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frames per second for output video (default: 30, use 60 for 2x speed)'
    )
    
    parser.add_argument(
        '--bitrate', '-b',
        type=int,
        default=5000,
        help='Video bitrate in kbps (default: 5000). Recommended: SD=2000, HD=5000, FHD=8000, 4K=20000'
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
    print(f"Density: {args.density}")
    print(f"Effect: {args.effect}")
    print(f"FPS: {args.fps}")
    print(f"Show Axes: {args.axes}")
    print(f"Show Formulas: {args.formulas}")
    print(f"Output: {args.output}")
    print("=" * 60)
    
    try:
        create_animation(
            resolution=args.resolution,
            dpi=args.dpi,
            density=args.density,
            effect=args.effect,
            show_axes=args.axes,
            show_formulas=args.formulas,
            fps=args.fps,
            bitrate=args.bitrate,
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

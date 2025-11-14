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
import json


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


def setup_figure(resolution='medium', dpi=100, show_axes=True, show_formulas=True, watermark='VUHUNG'):
    """
    Set up the matplotlib figure and 3D axes.
    
    Parameters:
    - resolution: 'small', 'medium', or 'large'
    - dpi: Dots per inch for the figure
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    - watermark: Watermark text to display (empty string for no watermark)
    
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
    
    # Force equal aspect ratio for 3D plot to fill screen properly
    ax.set_box_aspect([1, 1, 1])
    
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
    
    # Add watermark if provided
    if watermark:
        # Very dark color (close to black background) - nearly invisible but visible
        # Using a very dark gray (#050505) that's slightly lighter than pure black
        # with low alpha to make it subtle and non-intrusive
        fig.text(0.5, 0.5, watermark,
                transform=fig.transFigure,
                fontsize=14,  # Medium size
                verticalalignment='center',
                horizontalalignment='center',
                color='#050505',  # Very dark gray, nearly invisible
                alpha=0.25,  # Low transparency for subtlety - nearly invisible but visible
                weight='normal')
    
    return fig, ax


def get_beat_intensity(current_time, beat_times, window=0.1):
    """
    Check if there's a beat near current_time.
    Returns intensity (0-1) based on proximity to nearest beat.
    """
    if not beat_times or len(beat_times) == 0:
        return 0.0
    
    # Find nearest beat
    distances = np.abs(np.array(beat_times) - current_time)
    nearest_idx = np.argmin(distances)
    nearest_distance = distances[nearest_idx]
    
    # If within window, return intensity (closer = stronger)
    if nearest_distance < window:
        intensity = 1.0 - (nearest_distance / window)
        return float(intensity)
    return 0.0


def get_onset_intensity(current_time, onset_times, window=0.15):
    """Check if there's an onset near current_time."""
    if not onset_times or len(onset_times) == 0:
        return 0.0
    
    distances = np.abs(np.array(onset_times) - current_time)
    nearest_distance = np.min(distances)
    
    if nearest_distance < window:
        intensity = 1.0 - (nearest_distance / window)
        return float(intensity)
    return 0.0


def get_loudness_at_time(current_time, rms_times, rms_values):
    """Get normalized loudness (0-1) at current_time."""
    if not rms_times or not rms_values or len(rms_times) == 0:
        return 0.5
    
    # Find nearest RMS measurement
    distances = np.abs(np.array(rms_times) - current_time)
    idx = np.argmin(distances)
    return float(rms_values[idx])


def get_bass_at_time(current_time, bass_times, bass_values):
    """Get bass strength (0-1) at current_time."""
    if not bass_times or not bass_values or len(bass_times) == 0:
        return 0.5
    
    distances = np.abs(np.array(bass_times) - current_time)
    idx = np.argmin(distances)
    return float(bass_values[idx])


def get_tempo_at_time(current_time, tempo_times, tempo_values):
    """Get tempo (BPM) at current_time."""
    if not tempo_times or not tempo_values or len(tempo_times) == 0:
        return 120.0  # Default
    
    distances = np.abs(np.array(tempo_times) - current_time)
    idx = np.argmin(distances)
    return float(tempo_values[idx])


def create_animation(resolution='medium', dpi=100, density='high', effect='A',
                    show_axes=False, show_formulas=False, fps=30, bitrate=5000, output_path='outputs/heart_animation.mp4', watermark='VUHUNG', audio_features_path=None):
    """
    Create and save the 3D heart rotation animation.
    
    Parameters:
    - resolution: 'small', 'medium', 'large', or '4k'
    - dpi: Dots per inch for the figure
    - density: Point density ('lower', 'low', 'medium', 'high')
    - effect: Animation effect ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7')
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    - fps: Frames per second for output video (default: 30)
    - bitrate: Video bitrate in kbps (default: 5000)
    - output_path: Path to save the output video
    - watermark: Watermark text to display (default: 'VUHUNG', empty string for no watermark)
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
        'G2': 'Epic Heart Story (fade in/out + formulas + through heart + orbit - 137s)',
        'H1': 'Heart Genesis (creation story - 100s)',
        'H2': 'Time Reversal (forward then backward - 90s)',
        'H3': 'Fractal Heart (recursive hearts - 90s)',
        'H4': 'Dual Hearts (two hearts dancing - 120s)',
        'H5': 'Kaleidoscope Heart (mirrored reflections - 60s)',
        'H6': 'Heart Nebula (cosmic space journey - 120s)',
        'H7': 'Hologram Heart (wireframe tech aesthetic - 90s)',
        'H8': 'Heart Genesis with Music Sync (creation story with BPM-synchronized beats - 100s)',
        'H8sync': 'Heart Genesis with Real Audio Sync (creation story with librosa-detected beats - 100s)'
    }
    print(f"Generating heart shape with {point_counts.get(density, '40,000')} points (density: {density})...")
    print(f"Effect: {effect} - {effect_names.get(effect, 'Simple Y-axis rotation')}")
    
    # Load audio features if provided
    audio_features = None
    if audio_features_path and os.path.exists(audio_features_path):
        try:
            with open(audio_features_path, 'r') as f:
                audio_features = json.load(f)
            print(f"Loaded audio features: {len(audio_features.get('beat_times', []))} beats, {len(audio_features.get('onset_times', []))} onsets")
            if 'tempo_global' in audio_features:
                print(f"  Global tempo: {audio_features['tempo_global']:.1f} BPM")
        except Exception as e:
            print(f"Warning: Could not load audio features from {audio_features_path}: {e}")
            print("  Continuing without audio synchronization...")
            audio_features = None
    elif audio_features_path:
        print(f"Warning: Audio features file not found: {audio_features_path}")
        print("  Continuing without audio synchronization...")
    
    x_original, y_original, z_original, colors = generate_heart_points(density=density)
    
    print(f"Setting up figure with resolution: {resolution}, DPI: {dpi}")
    fig, ax = setup_figure(resolution, dpi, show_axes, show_formulas, watermark)
    
    # Generate second heart for H4 effect (dual hearts)
    if effect == 'H4':
        x_heart2, y_heart2, z_heart2, colors2 = generate_heart_points(density=density)
    else:
        x_heart2, y_heart2, z_heart2, colors2 = None, None, None, None
    
    # Initial scatter plot
    scatter = ax.scatter(x_original, y_original, z_original, 
                        c=colors, cmap='magma', s=1, alpha=0.8)
    
    # Set axis limits to keep the heart centered with equal aspect ratio
    max_range = 20
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Total frames - adjust for longer effects
    if effect == 'G1':
        total_frames = 2700  # 90 seconds at 30 fps for G1
        duration_text = "90 seconds"
    elif effect == 'G2':
        total_frames = 4110  # 137 seconds at 30 fps for G2
        duration_text = "137 seconds"
    elif effect == 'H1':
        total_frames = 3000  # 100 seconds at 30 fps for H1
        duration_text = "100 seconds"
    elif effect == 'H8':
        total_frames = 3000  # 100 seconds at 30 fps for H8
        duration_text = "100 seconds"
    elif effect == 'H8sync':
        total_frames = 3000  # 100 seconds at 30 fps for H8sync
        duration_text = "100 seconds"
    elif effect == 'H2':
        total_frames = 2700  # 90 seconds at 30 fps for H2
        duration_text = "90 seconds"
    elif effect == 'H3':
        total_frames = 2700  # 90 seconds at 30 fps for H3
        duration_text = "90 seconds"
    elif effect == 'H4':
        total_frames = 3600  # 120 seconds at 30 fps for H4
        duration_text = "120 seconds"
    elif effect == 'H5':
        total_frames = 1800  # 60 seconds at 30 fps for H5
        duration_text = "60 seconds"
    elif effect == 'H6':
        total_frames = 3600  # 120 seconds at 30 fps for H6
        duration_text = "120 seconds"
    elif effect == 'H7':
        total_frames = 2700  # 90 seconds at 30 fps for H7
        duration_text = "90 seconds"
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
            
            ax.set_xlim([-zoom_factor, zoom_factor])
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
            ax.set_xlim([-zoom_factor, zoom_factor])
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
            ax.set_xlim([-zoom_factor, zoom_factor])
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
            ax.set_xlim([-zoom_factor, zoom_factor])
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
            ax.set_xlim([-zoom_factor, zoom_factor])
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
            
            # Apply alpha and position
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H1: Heart Genesis (creation story - 100 seconds)
        elif effect == 'H1':
            current_second = frame / 30.0
            
            # Heart rotates slowly (180 degrees total)
            alpha_deg = frame * 180 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            point_alpha = 0.8
            
            # Phase 1 (0-10s): Empty black space with single point of light
            if current_second < 10.0:
                phase_t = current_second / 10.0
                point_alpha = 0.0  # Heart invisible
                zoom_factor = 200  # Very far
                elevation = 20
                azimuth = 45
                # Could add a single point of light here (would need additional scatter)
            
            # Phase 2 (10-25s): Point explodes into scattered particles forming heart shape
            elif current_second < 25.0:
                phase_t = (current_second - 10.0) / 15.0
                # Gradually reveal heart with particle-like effect (alpha fade in)
                point_alpha = 0.8 * phase_t
                # Scale from very small to normal
                scale = 0.1 + 0.9 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
                zoom_factor = 25 - 5 * phase_t  # Zoom in
                elevation = 20
                azimuth = 45
            
            # Phase 3 (25-40s): Particles coalesce, heart materializes with increasing density
            elif current_second < 40.0:
                phase_t = (current_second - 25.0) / 15.0
                point_alpha = 0.8
                zoom_factor = 20 - 3 * phase_t  # Continue zooming
                elevation = 20 + 10 * np.sin(np.pi * phase_t)
                azimuth = 45 + 90 * phase_t
            
            # Phase 4 (40-60s): Fully formed heart pulses to life (first heartbeat)
            elif current_second < 60.0:
                phase_t = (current_second - 40.0) / 20.0
                point_alpha = 0.8
                # Heartbeat pulse
                heartbeat = 1.0 + 0.2 * np.sin(2 * np.pi * 2 * phase_t) ** 2
                x_rotated = x_rotated * heartbeat
                y_rotated = y_rotated * heartbeat
                z_rotated = z_rotated * heartbeat
                zoom_factor = 17
                elevation = 20
                azimuth = 45 + 180 * phase_t
            
            # Phase 5 (60-75s): Heart rotates majestically, showing its beauty
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                point_alpha = 0.8
                zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
                elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
                azimuth = 225 + 360 * phase_t
            
            # Phase 6 (75-90s): Zoom out to cosmic scale, heart glows like a star
            elif current_second < 90.0:
                phase_t = (current_second - 75.0) / 15.0
                point_alpha = 0.8 + 0.2 * phase_t  # Glow effect (brighter)
                zoom_factor = 20 + 80 * phase_t  # Zoom out dramatically
                elevation = 40 - 20 * phase_t
                azimuth = 585 + 90 * phase_t
            
            # Phase 7 (90-95s): Fade formulas in as "blueprint of creation"
            elif current_second < 95.0:
                phase_t = (current_second - 90.0) / 5.0
                point_alpha = 1.0  # Fully bright
                zoom_factor = 100
                elevation = 20
                azimuth = 675
                # Formulas handled by show_formulas flag
            
            # Phase 8 (95-100s): Fade to infinite stars, one becomes the heart again
            else:
                phase_t = (current_second - 95.0) / 5.0
                point_alpha = 1.0 * (1.0 - phase_t)  # Fade out
                zoom_factor = 100 + 100 * phase_t
                elevation = 20
                azimuth = 675
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H8: Heart Genesis with Music Sync (BPM-synchronized beats - 100 seconds)
        elif effect == 'H8':
            current_second = frame / 30.0
            
            # Heart rotates slowly (180 degrees total)
            alpha_deg = frame * 180 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_base = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_base = y_original
            z_base = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Base scale (no heartbeat yet)
            heartbeat_scale = 1.0
            
            # Calculate heartbeat pulses at BPM transition points
            # Each heartbeat is a quick pulse (0.3 seconds) at the transition
            heartbeat_duration = 0.3  # 0.3 seconds for each heartbeat
            
            # BPM transition points where heartbeats occur
            if abs(current_second - 10.0) < heartbeat_duration:  # 60→75 BPM at 0:10
                beat_t = abs(current_second - 10.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)  # Quick pulse
            elif abs(current_second - 25.0) < heartbeat_duration:  # 75→80 BPM at 0:25
                beat_t = abs(current_second - 25.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            elif abs(current_second - 40.0) < heartbeat_duration:  # 80→85 BPM at 0:40
                beat_t = abs(current_second - 40.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            elif abs(current_second - 60.0) < heartbeat_duration:  # 85→90 BPM at 1:00
                beat_t = abs(current_second - 60.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            elif abs(current_second - 75.0) < heartbeat_duration:  # 90→75 BPM at 1:15
                beat_t = abs(current_second - 75.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            elif abs(current_second - 90.0) < heartbeat_duration:  # 75→70 BPM at 1:30
                beat_t = abs(current_second - 90.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            elif abs(current_second - 95.0) < heartbeat_duration:  # 70→60 BPM at 1:35
                beat_t = abs(current_second - 95.0) / heartbeat_duration
                heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
            
            # Apply heartbeat scale
            x_rotated = x_base * heartbeat_scale
            y_rotated = y_base * heartbeat_scale
            z_rotated = z_base * heartbeat_scale
            
            point_alpha = 0.8
            
            # Phase 1 (0-10s): Empty black space, then gradually heart appears
            if current_second < 10.0:
                phase_t = current_second / 10.0
                # Gradually fade in from blank
                point_alpha = 0.8 * phase_t
                # Scale from very small to normal
                scale = 0.1 + 0.9 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
                zoom_factor = 200 - 175 * phase_t  # Start very far, approach
                elevation = 20
                azimuth = 45
            
            # Phase 2 (10-25s): Energy burst, strings ascending
            elif current_second < 25.0:
                phase_t = (current_second - 10.0) / 15.0
                point_alpha = 0.8
                zoom_factor = 25 - 5 * phase_t  # Continue zooming in
                elevation = 20
                azimuth = 45 + 90 * phase_t
            
            # Phase 3 (25-40s): Strings coalesce, 80 BPM
            elif current_second < 40.0:
                phase_t = (current_second - 25.0) / 15.0
                point_alpha = 0.8
                zoom_factor = 20 - 3 * phase_t  # Continue zooming
                elevation = 20 + 10 * np.sin(np.pi * phase_t)
                azimuth = 135 + 90 * phase_t
            
            # Phase 4 (40-60s): Heartbeat rhythm, 85 BPM
            elif current_second < 60.0:
                phase_t = (current_second - 40.0) / 20.0
                point_alpha = 0.8
                zoom_factor = 17
                elevation = 20
                azimuth = 225 + 180 * phase_t
            
            # Phase 5 (60-75s): Majestic orchestral, 90 BPM
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                point_alpha = 0.8
                zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
                elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
                azimuth = 405 + 360 * phase_t
            
            # Phase 6 (75-90s): Cosmic expansion, 75 BPM
            elif current_second < 90.0:
                phase_t = (current_second - 75.0) / 15.0
                point_alpha = 0.8 + 0.2 * phase_t  # Glow effect
                zoom_factor = 20 + 80 * phase_t  # Zoom out dramatically
                elevation = 40 - 20 * phase_t
                azimuth = 585 + 90 * phase_t
            
            # Phase 7 (90-95s): Mathematical precision, 70 BPM
            elif current_second < 95.0:
                phase_t = (current_second - 90.0) / 5.0
                point_alpha = 1.0  # Fully bright
                zoom_factor = 100
                elevation = 20
                azimuth = 675
            
            # Phase 8 (95-100s): Fade to silence, 60 BPM, infinite stars
            else:
                phase_t = (current_second - 95.0) / 5.0
                point_alpha = 1.0 * (1.0 - phase_t)  # Fade out
                zoom_factor = 100 + 100 * phase_t
                elevation = 20
                azimuth = 675
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H8sync: Heart Genesis with Real Audio Sync (using librosa-detected features - 100 seconds)
        elif effect == 'H8sync':
            current_second = frame / 30.0
            
            # Load audio features if available
            if audio_features:
                beat_times = audio_features.get('beat_times', [])
                onset_times = audio_features.get('onset_times', [])
                rms_times = audio_features.get('rms_times', [])
                rms_values = audio_features.get('rms_values', [])
                bass_times = audio_features.get('bass_times', [])
                bass_values = audio_features.get('bass_values', [])
                tempo_times = audio_features.get('tempo_times', [])
                tempo_values = audio_features.get('tempo_values', [])
                
                # Get current audio features
                beat_intensity = get_beat_intensity(current_second, beat_times, window=0.1)
                onset_intensity = get_onset_intensity(current_second, onset_times, window=0.15)
                loudness = get_loudness_at_time(current_second, rms_times, rms_values)
                bass = get_bass_at_time(current_second, bass_times, bass_values)
                current_tempo = get_tempo_at_time(current_second, tempo_times, tempo_values)
            else:
                # Fallback to hardcoded values if no audio features
                beat_intensity = 0.0
                onset_intensity = 0.0
                loudness = 0.5
                bass = 0.5
                current_tempo = 75.0
            
            # Heart rotates slowly (180 degrees total, tempo-adjusted)
            # Adjust rotation speed based on tempo (faster tempo = faster rotation)
            tempo_factor = current_tempo / 75.0  # Normalize to 75 BPM baseline
            alpha_deg = frame * 180 * tempo_factor / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            x_base = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_base = y_original
            z_base = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Heartbeat pulse synchronized with beats
            heartbeat_scale = 1.0
            if beat_intensity > 0:
                # Pulse on beat: stronger beat = bigger pulse
                heartbeat_scale = 1.0 + 0.2 * beat_intensity
            
            # Also pulse on strong onsets
            if onset_intensity > 0.5:
                heartbeat_scale = max(heartbeat_scale, 1.0 + 0.15 * onset_intensity)
            
            # Apply heartbeat
            x_rotated = x_base * heartbeat_scale
            y_rotated = y_base * heartbeat_scale
            z_rotated = z_base * heartbeat_scale
            
            point_alpha = 0.8
            
            # Phase 1 (0-10s): Empty black space, then gradually heart appears
            if current_second < 10.0:
                phase_t = current_second / 10.0
                # Gradually fade in from blank
                point_alpha = 0.8 * phase_t
                # Scale from very small to normal
                scale = 0.1 + 0.9 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
                # Adjust zoom based on loudness (louder = closer)
                base_zoom = 200 - 175 * phase_t
                zoom_factor = base_zoom - 5 * loudness  # Louder = zoom in more
                elevation = 20
                azimuth = 45
            
            # Phase 2 (10-25s): Energy burst, strings ascending
            elif current_second < 25.0:
                phase_t = (current_second - 10.0) / 15.0
                point_alpha = 0.8
                # Zoom based on loudness
                base_zoom = 25 - 5 * phase_t
                zoom_factor = base_zoom - 5 * loudness
                elevation = 20
                azimuth = 45 + 90 * phase_t
            
            # Phase 3 (25-40s): Strings coalesce
            elif current_second < 40.0:
                phase_t = (current_second - 25.0) / 15.0
                point_alpha = 0.8
                base_zoom = 20 - 3 * phase_t
                zoom_factor = base_zoom - 5 * loudness
                elevation = 20 + 10 * np.sin(np.pi * phase_t)
                azimuth = 135 + 90 * phase_t
            
            # Phase 4 (40-60s): Heartbeat rhythm
            elif current_second < 60.0:
                phase_t = (current_second - 40.0) / 20.0
                point_alpha = 0.8
                # Zoom based on loudness
                zoom_factor = 17 - 5 * loudness
                elevation = 20
                azimuth = 225 + 180 * phase_t
            
            # Phase 5 (60-75s): Majestic orchestral
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                point_alpha = 0.8
                base_zoom = 17 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 5 * loudness
                elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
                azimuth = 405 + 360 * phase_t
            
            # Phase 6 (75-90s): Cosmic expansion
            elif current_second < 90.0:
                phase_t = (current_second - 75.0) / 15.0
                # Adjust alpha based on bass (more bass = brighter)
                point_alpha = 0.6 + 0.4 * bass + 0.2 * phase_t  # Glow effect
                point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
                base_zoom = 20 + 80 * phase_t
                zoom_factor = base_zoom - 5 * loudness
                elevation = 40 - 20 * phase_t
                azimuth = 585 + 90 * phase_t
            
            # Phase 7 (90-95s): Mathematical precision
            elif current_second < 95.0:
                phase_t = (current_second - 90.0) / 5.0
                point_alpha = 0.6 + 0.4 * bass  # Fully bright based on bass
                point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
                zoom_factor = 100 - 5 * loudness
                elevation = 20
                azimuth = 675
            
            # Phase 8 (95-100s): Fade to silence, infinite stars
            else:
                phase_t = (current_second - 95.0) / 5.0
                point_alpha = (0.6 + 0.4 * bass) * (1.0 - phase_t)  # Fade out
                point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
                base_zoom = 100 + 100 * phase_t
                zoom_factor = base_zoom - 5 * loudness
                elevation = 20
                azimuth = 675
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H2: Time Reversal (forward then backward - 90 seconds)
        elif effect == 'H2':
            current_second = frame / 30.0
            
            # Phase 1 (0-45s): Normal G2-style journey forward
            if current_second < 45.0:
                phase_t = current_second / 45.0
                # Rotate heart
                alpha_deg = frame * 270 / (total_frames // 2)
                alpha_rad = np.deg2rad(alpha_deg)
                x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
                y_rotated = y_original
                z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
                
                # Camera motion
                zoom_factor = 20 - 10 * phase_t + 5 * np.sin(4 * np.pi * phase_t)
                elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
                azimuth = 45 + 360 * phase_t
                point_alpha = 0.8
                
            # Phase 2 (45-48s): Freeze frame at peak moment
            elif current_second < 48.0:
                alpha_deg = (total_frames // 2) * 270 / (total_frames // 2)
                alpha_rad = np.deg2rad(alpha_deg)
                x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
                y_rotated = y_original
                z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
                
                zoom_factor = 15
                elevation = 35
                azimuth = 405
                point_alpha = 0.8
            
            # Phase 3 (48-90s): Reverse time - everything plays backward
            else:
                reverse_t = (current_second - 48.0) / 42.0
                reverse_frame = int((1.0 - reverse_t) * (total_frames // 2))
                
                # Rotate heart backward
                alpha_deg = reverse_frame * 270 / (total_frames // 2)
                alpha_rad = np.deg2rad(alpha_deg)
                x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
                y_rotated = y_original
                z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
                
                # Camera motion backward
                phase_t = 1.0 - reverse_t
                zoom_factor = 20 - 10 * phase_t + 5 * np.sin(4 * np.pi * phase_t)
                elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
                azimuth = 45 + 360 * phase_t
                point_alpha = 0.8
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H3: Fractal Heart (recursive hearts - 90 seconds)
        elif effect == 'H3':
            current_second = frame / 30.0
            
            # Rotate main heart
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            point_alpha = 0.8
            
            # Phase 1 (0-15s): Start with normal heart
            if current_second < 15.0:
                zoom_factor = 20
                elevation = 20
                azimuth = 45 + 180 * (current_second / 15.0)
            
            # Phase 2 (15-45s): Zoom into heart center, discover smaller heart inside
            elif current_second < 45.0:
                phase_t = (current_second - 15.0) / 30.0
                # Zoom in dramatically
                zoom_factor = 20 - 18 * phase_t  # 20 to 2
                elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 225 + 360 * phase_t
                # Visual effect: scale down to show "inner heart"
                scale = 1.0 - 0.5 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
            
            # Phase 3 (45-60s): Zoom into that heart, find another (3-5 levels)
            elif current_second < 60.0:
                phase_t = (current_second - 45.0) / 15.0
                zoom_factor = 2 - 1.5 * phase_t  # 2 to 0.5
                elevation = 30 + 10 * np.sin(4 * np.pi * phase_t)
                azimuth = 585 + 360 * phase_t
                scale = 0.5 - 0.3 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
            
            # Phase 4 (60-75s): Zoom back out through all levels
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                zoom_factor = 0.5 + 19.5 * phase_t  # 0.5 to 20
                elevation = 40 - 20 * phase_t
                azimuth = 945 - 720 * phase_t
                scale = 0.2 + 0.8 * phase_t
                x_rotated = x_rotated * scale
                y_rotated = y_rotated * scale
                z_rotated = z_rotated * scale
            
            # Phase 5 (75-90s): Final reveal - the universe is made of hearts
            else:
                phase_t = (current_second - 75.0) / 15.0
                zoom_factor = 20 + 30 * phase_t  # Zoom out to cosmic scale
                elevation = 20
                azimuth = 225 + 180 * phase_t
                # Return to normal scale
                x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
                y_rotated = y_original
                z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H4: Dual Hearts (two hearts dancing - 120 seconds)
        elif effect == 'H4':
            current_second = frame / 30.0
            
            # Rotate both hearts
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            # Heart 1 (original)
            x1 = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y1 = y_original
            z1 = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            # Heart 2 (offset and rotated)
            x2 = x_heart2 * np.cos(alpha_rad + np.pi/4) + z_heart2 * np.sin(alpha_rad + np.pi/4)
            y2 = y_heart2
            z2 = -x_heart2 * np.sin(alpha_rad + np.pi/4) + z_heart2 * np.cos(alpha_rad + np.pi/4)
            
            # Phase 1 (0-15s): First heart appears
            if current_second < 15.0:
                phase_t = current_second / 15.0
                # Only show heart 1, fade in
                point_alpha = 0.8 * phase_t
                # Position heart 1
                offset = 0
                x_rotated = x1 + offset
                y_rotated = y1
                z_rotated = z1
                zoom_factor = 30 - 10 * phase_t
                elevation = 20
                azimuth = 45
            
            # Phase 2 (15-30s): Second heart appears
            elif current_second < 30.0:
                phase_t = (current_second - 15.0) / 15.0
                point_alpha = 0.8
                # Combine both hearts with offset
                offset1 = -8 * (1.0 - phase_t)
                offset2 = 8 * phase_t
                x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1, z2])
                zoom_factor = 20
                elevation = 20
                azimuth = 45 + 90 * phase_t
            
            # Phase 3 (30-60s): Hearts orbit each other like binary stars
            elif current_second < 60.0:
                phase_t = (current_second - 30.0) / 30.0
                point_alpha = 0.8
                orbit_radius = 8
                angle = 2 * np.pi * phase_t
                offset1 = orbit_radius * np.cos(angle)
                offset2 = orbit_radius * np.cos(angle + np.pi)
                x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
                zoom_factor = 25
                elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 135 + 360 * phase_t
            
            # Phase 4 (60-75s): Hearts spiral closer
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                point_alpha = 0.8
                orbit_radius = 8 * (1.0 - phase_t)  # Spiral in
                angle = 2 * np.pi * phase_t * 2
                offset1 = orbit_radius * np.cos(angle)
                offset2 = orbit_radius * np.cos(angle + np.pi)
                x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
                zoom_factor = 20 - 5 * phase_t
                elevation = 30 - 10 * phase_t
                azimuth = 495 + 180 * phase_t
            
            # Phase 5 (75-85s): Hearts briefly merge/overlap
            elif current_second < 85.0:
                phase_t = (current_second - 75.0) / 10.0
                point_alpha = 0.8 + 0.2 * np.sin(4 * np.pi * phase_t)  # Pulse
                # Hearts at same position
                x_rotated = np.concatenate([x1, x2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1, z2])
                zoom_factor = 15
                elevation = 20
                azimuth = 675 + 90 * phase_t
            
            # Phase 6 (85-95s): Hearts separate but remain connected by "thread"
            elif current_second < 95.0:
                phase_t = (current_second - 85.0) / 10.0
                point_alpha = 0.8
                separation = 4 * phase_t
                x_rotated = np.concatenate([x1 - separation, x2 + separation])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1, z2])
                zoom_factor = 15 + 5 * phase_t
                elevation = 20
                azimuth = 765 + 90 * phase_t
            
            # Phase 7 (95-105s): Final orbit, synchronized rotation
            elif current_second < 105.0:
                phase_t = (current_second - 95.0) / 10.0
                point_alpha = 0.8
                orbit_radius = 4 + 4 * phase_t
                angle = 2 * np.pi * phase_t
                offset1 = orbit_radius * np.cos(angle)
                offset2 = orbit_radius * np.cos(angle + np.pi)
                x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
                zoom_factor = 20
                elevation = 20 + 5 * np.sin(4 * np.pi * phase_t)
                azimuth = 855 + 360 * phase_t
            
            # Phase 8 (105-120s): Fade to black, showing connection line last
            else:
                phase_t = (current_second - 105.0) / 15.0
                point_alpha = 0.8 * (1.0 - phase_t)
                orbit_radius = 8
                angle = 2 * np.pi * (1.0 + phase_t)
                offset1 = orbit_radius * np.cos(angle)
                offset2 = orbit_radius * np.cos(angle + np.pi)
                x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
                y_rotated = np.concatenate([y1, y2])
                z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
                zoom_factor = 20 + 10 * phase_t
                elevation = 25
                azimuth = 1215
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H5: Kaleidoscope Heart (mirrored reflections - 60 seconds)
        elif effect == 'H5':
            # Rotate heart
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            current_second = frame / 30.0
            point_alpha = 0.8
            
            # Create mirrored versions
            # Phase 1 (0-10s): Single heart in center
            if current_second < 10.0:
                zoom_factor = 20
                elevation = 20
                azimuth = 45 + 180 * (current_second / 10.0)
            
            # Phase 2 (10-25s): Mirrors appear (4 quadrants)
            elif current_second < 25.0:
                phase_t = (current_second - 10.0) / 15.0
                # Create 4 mirrored hearts
                x_all = np.concatenate([
                    x_rotated,  # Original
                    -x_rotated,  # Mirror X
                    x_rotated,  # Mirror Y
                    -x_rotated,  # Mirror both
                ])
                y_all = np.concatenate([y_rotated, y_rotated, -y_rotated, -y_rotated])
                z_all = np.concatenate([z_rotated, -z_rotated, z_rotated, -z_rotated])
                
                # Fade in mirrors
                if phase_t < 0.5:
                    point_alpha = 0.8 * (phase_t * 2)
                else:
                    point_alpha = 0.8
                
                x_rotated = x_all
                y_rotated = y_all
                z_rotated = z_all
                zoom_factor = 25
                elevation = 20
                azimuth = 225 + 180 * phase_t
            
            # Phase 3 (25-40s): 8 mirrors (add diagonal)
            elif current_second < 40.0:
                phase_t = (current_second - 25.0) / 15.0
                # 8 hearts in octagon pattern
                angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
                x_all = []
                y_all = []
                z_all = []
                for angle in angles:
                    cos_a = np.cos(angle)
                    sin_a = np.sin(angle)
                    x_mirror = x_rotated * cos_a - z_rotated * sin_a
                    z_mirror = x_rotated * sin_a + z_rotated * cos_a
                    x_all.append(x_mirror)
                    y_all.append(y_rotated)
                    z_all.append(z_mirror)
                
                x_rotated = np.concatenate(x_all)
                y_rotated = np.concatenate(y_all)
                z_rotated = np.concatenate(z_all)
                zoom_factor = 30
                elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 405 + 360 * phase_t
            
            # Phase 4 (40-50s): 16 mirrors (mandala pattern)
            elif current_second < 50.0:
                phase_t = (current_second - 40.0) / 10.0
                # 16 hearts
                angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
                x_all = []
                y_all = []
                z_all = []
                for angle in angles:
                    cos_a = np.cos(angle)
                    sin_a = np.sin(angle)
                    x_mirror = x_rotated * cos_a - z_rotated * sin_a
                    z_mirror = x_rotated * sin_a + z_rotated * cos_a
                    x_all.append(x_mirror)
                    y_all.append(y_rotated)
                    z_all.append(z_mirror)
                
                x_rotated = np.concatenate(x_all)
                y_rotated = np.concatenate(y_all)
                z_rotated = np.concatenate(z_all)
                zoom_factor = 35
                elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
                azimuth = 765 + 720 * phase_t
            
            # Phase 5 (50-55s): Pattern collapses back to single heart
            elif current_second < 55.0:
                phase_t = (current_second - 50.0) / 5.0
                point_alpha = 0.8 * (1.0 - phase_t)
                zoom_factor = 35 - 15 * phase_t
                elevation = 35 - 15 * phase_t
                azimuth = 1485 - 1440 * phase_t
            
            # Phase 6 (55-60s): Final reveal - was always one heart
            else:
                phase_t = (current_second - 55.0) / 5.0
                point_alpha = 0.8 * phase_t
                zoom_factor = 20
                elevation = 20
                azimuth = 45
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H6: Heart Nebula (cosmic space journey - 120 seconds)
        elif effect == 'H6':
            current_second = frame / 30.0
            
            # Rotate heart slowly
            alpha_deg = frame * 180 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            point_alpha = 0.8
            
            # Phase 1 (0-15s): Start in deep space (distant heart glows like galaxy)
            if current_second < 15.0:
                phase_t = current_second / 15.0
                point_alpha = 0.3 + 0.5 * phase_t  # Glow effect
                zoom_factor = 200 - 150 * phase_t  # Very far to closer
                elevation = 20
                azimuth = 45
            
            # Phase 2 (15-45s): Travel through stars toward heart-nebula
            elif current_second < 45.0:
                phase_t = (current_second - 15.0) / 30.0
                point_alpha = 0.8 + 0.2 * np.sin(4 * np.pi * phase_t)  # Pulsing glow
                zoom_factor = 50 - 30 * phase_t  # Continue approaching
                elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 45 + 180 * phase_t
            
            # Phase 3 (45-60s): Pass through "cosmic dust" (particle effects)
            elif current_second < 60.0:
                phase_t = (current_second - 45.0) / 15.0
                point_alpha = 0.8 + 0.2 * np.sin(8 * np.pi * phase_t)  # Rapid pulsing
                zoom_factor = 20 - 5 * phase_t  # Get very close
                elevation = 30 - 10 * phase_t
                azimuth = 225 + 90 * phase_t
            
            # Phase 4 (60-75s): Arrive at heart, now massive and glowing
            elif current_second < 75.0:
                phase_t = (current_second - 60.0) / 15.0
                point_alpha = 1.0  # Fully bright
                zoom_factor = 15 + 2 * np.sin(2 * np.pi * phase_t)
                elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
                azimuth = 315 + 180 * phase_t
            
            # Phase 5 (75-90s): Orbit around heart-planet
            elif current_second < 90.0:
                phase_t = (current_second - 75.0) / 15.0
                point_alpha = 1.0
                zoom_factor = 17
                elevation = 20 + 25 * np.sin(2 * np.pi * phase_t)
                azimuth = 495 + 360 * phase_t
            
            # Phase 6 (90-105s): See other "heart planets" in distance
            elif current_second < 105.0:
                phase_t = (current_second - 90.0) / 15.0
                point_alpha = 1.0
                zoom_factor = 17 + 20 * phase_t  # Zoom out to see others
                elevation = 45 - 25 * phase_t
                azimuth = 855 + 180 * phase_t
            
            # Phase 7 (105-120s): Zoom out - our heart is one of many in "heart galaxy"
            else:
                phase_t = (current_second - 105.0) / 15.0
                point_alpha = 1.0 - 0.2 * phase_t  # Slight fade
                zoom_factor = 37 + 163 * phase_t  # Zoom out dramatically
                elevation = 20
                azimuth = 1035 + 90 * phase_t
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
            ax.set_ylim([-zoom_factor, zoom_factor])
            ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Effect H7: Hologram Heart (wireframe tech aesthetic - 90 seconds)
        elif effect == 'H7':
            current_second = frame / 30.0
            
            # Rotate heart
            alpha_deg = frame * 360 / total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            
            point_alpha = 0.8
            
            # Phase 1 (0-10s): Grid floor and walls appear (tron-style)
            if current_second < 10.0:
                phase_t = current_second / 10.0
                point_alpha = 0.0  # Heart invisible initially
                zoom_factor = 30
                elevation = 20
                azimuth = 45
            
            # Phase 2 (10-20s): Heart materializes as wireframe
            elif current_second < 20.0:
                phase_t = (current_second - 10.0) / 10.0
                point_alpha = 0.3 * phase_t  # Wireframe effect (low alpha)
                zoom_factor = 30 - 10 * phase_t
                elevation = 20
                azimuth = 45 + 90 * phase_t
            
            # Phase 3 (20-35s): Wireframe fills in with points progressively
            elif current_second < 35.0:
                phase_t = (current_second - 20.0) / 15.0
                point_alpha = 0.3 + 0.5 * phase_t  # Gradually fill
                zoom_factor = 20
                elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 135 + 180 * phase_t
            
            # Phase 4 (35-50s): Hologram "glitches" and reforms
            elif current_second < 50.0:
                phase_t = (current_second - 35.0) / 15.0
                # Glitch effect: random alpha fluctuations
                glitch = 0.1 * np.sin(20 * np.pi * phase_t) * np.sin(7 * np.pi * phase_t)
                point_alpha = 0.8 + glitch
                point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
                zoom_factor = 20 + 3 * np.sin(4 * np.pi * phase_t)
                elevation = 30 - 10 * np.sin(2 * np.pi * phase_t)
                azimuth = 315 + 360 * phase_t
            
            # Phase 5 (50-70s): Multiple holographic layers (like x-ray views)
            elif current_second < 70.0:
                phase_t = (current_second - 50.0) / 20.0
                point_alpha = 0.8 + 0.2 * np.sin(2 * np.pi * phase_t)
                zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
                elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
                azimuth = 675 + 540 * phase_t
            
            # Phase 6 (70-85s): Final solid form with scan lines effect
            elif current_second < 85.0:
                phase_t = (current_second - 70.0) / 15.0
                # Scan line effect: slight alpha variation
                scan_line = 0.1 * np.sin(10 * np.pi * phase_t)
                point_alpha = 1.0 + scan_line
                point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
                zoom_factor = 20
                elevation = 40 - 20 * phase_t
                azimuth = 1215 + 180 * phase_t
            
            # Phase 7 (85-90s): Hologram powers down in sections
            else:
                phase_t = (current_second - 85.0) / 5.0
                point_alpha = 1.0 * (1.0 - phase_t)  # Fade out
                zoom_factor = 20 + 10 * phase_t
                elevation = 20
                azimuth = 1395
            
            scatter.set_alpha(point_alpha)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            ax.view_init(elev=elevation, azim=azimuth)
            ax.set_xlim([-zoom_factor, zoom_factor])
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
    
    print(f"Animation successfully saved to {output_path}")
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
  H1 - Heart Genesis: Creation story from nothing to heart, with particle effects and cosmic scale (100 seconds)
  H2 - Time Reversal: Forward journey then backward with time echoes (90 seconds)
  H3 - Fractal Heart: Recursive hearts at different scales, zoom in and out (90 seconds)
  H4 - Dual Hearts: Two hearts dancing together, orbiting and merging (120 seconds)
  H5 - Kaleidoscope Heart: Mirrored reflections creating mandala patterns (60 seconds)
  H6 - Heart Nebula: Cosmic space journey with glowing heart as celestial body (120 seconds)
  H7 - Hologram Heart: Wireframe tech aesthetic with glitch effects (90 seconds)
  H8sync - Heart Genesis with Real Audio Sync: Creation story synchronized with librosa-detected beats, tempo, loudness, and bass (100 seconds, requires --audio-features)

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
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H8sync'],
        default='A',
        help='Animation effect: A (multi-axis), B (camera orbit), C (combined), D (custom), E (heartbeat), F (spiral), G (figure-8), G1 (journey 90s), G2 (epic story 137s), H1 (genesis 100s), H2 (time reversal 90s), H3 (fractal 90s), H4 (dual hearts 120s), H5 (kaleidoscope 60s), H6 (nebula 120s), H7 (hologram 90s), H8 (genesis with music sync 100s), H8sync (genesis with real audio sync 100s) (default: A)'
    )
    
    parser.add_argument(
        '--audio-features',
        dest='audio_features',
        help='Path to JSON file containing audio features (from analyze_audio.py). Required for H8sync effect.'
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
    
    parser.add_argument(
        '--watermark',
        default='VUHUNG',
        help='Watermark text to display at center of video (default: "VUHUNG"). Use --watermark "" to disable watermark.'
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
    print(f"Watermark: {args.watermark if args.watermark else '(disabled)'}")
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
            output_path=args.output,
            watermark=args.watermark,
            audio_features_path=args.audio_features
        )
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

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

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Import from new modular structure
from core.heart_generator import generate_heart_points
from core.figure_setup import setup_figure
from effects import get_effect_class


def create_animation(resolution='medium', dpi=100, density='high', effect='A',
                    show_axes=False, show_formulas=False, fps=30, bitrate=5000, 
                    output_path='outputs/heart_animation.mp4', watermark='VUHUNG', 
                    audio_features_path=None):
    """
    Create and save the 3D heart rotation animation.
    
    Parameters:
    - resolution: 'small', 'medium', 'large', or '4k'
    - dpi: Dots per inch for the figure
    - density: Point density ('lower', 'low', 'medium', 'high')
    - effect: Animation effect ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H8sync')
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    - fps: Frames per second for output video (default: 30)
    - bitrate: Video bitrate in kbps (default: 5000)
    - output_path: Path to save the output video
    - watermark: Watermark text to display (default: 'VUHUNG', empty string for no watermark)
    - audio_features_path: Path to JSON file with audio features (for H8sync)
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
        'H8sync': 'Heart Genesis with Real Audio Sync (creation story with librosa-detected beats - 100s)',
        'H8sync3min': 'Heart Genesis with Real Audio Sync - Extended 3.5 minute version (210s)',
        'H9': 'Cuba to New Orleans - Musical Journey Through the Heart with through-heart passages (~698s)',
        'H10': 'The Mission (Gabriel\'s Oboe) - Spiritual Journey Through the Heart with through-heart passages'
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
    
    # Generate heart points
    x_original, y_original, z_original, colors = generate_heart_points(density=density)
    
    print(f"Setting up figure with resolution: {resolution}, DPI: {dpi}")
    fig, ax = setup_figure(resolution, dpi, show_axes, show_formulas, watermark)
    
    # Generate second heart for H4 effect (dual hearts)
    x_heart2, y_heart2, z_heart2 = None, None, None
    if effect == 'H4':
        x_heart2, y_heart2, z_heart2, colors2 = generate_heart_points(density=density)
    
    # Initial scatter plot
    scatter = ax.scatter(x_original, y_original, z_original, 
                        c=colors, cmap='magma', s=1, alpha=0.8)
    
    # Set axis limits to keep the heart centered with equal aspect ratio
    max_range = 20
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    # Get effect class from registry
    EffectClass = get_effect_class(effect)
    if EffectClass is None:
        print(f"Warning: Effect '{effect}' not found in registry. Using default simple rotation.")
        # Fallback: simple rotation
        total_frames = 900
        duration_text = "30 seconds"
        
        def update(frame):
            t = frame / 900.0
            alpha_deg = frame * 360 / 900
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = x_original * np.cos(alpha_rad) + z_original * np.sin(alpha_rad)
            y_rotated = y_original
            z_rotated = -x_original * np.sin(alpha_rad) + z_original * np.cos(alpha_rad)
            scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
            return scatter,
    else:
        # Instantiate effect
        # For H4, pass second heart coordinates
        if effect == 'H4':
            effect_instance = EffectClass(
                total_frames=0,  # Will be set by get_total_frames
                fps=fps,
                x_original=x_original,
                y_original=y_original,
                z_original=z_original,
                scatter=scatter,
                ax=ax,
                audio_features=audio_features,
                x_heart2=x_heart2,
                y_heart2=y_heart2,
                z_heart2=z_heart2
            )
        else:
            effect_instance = EffectClass(
                total_frames=0,  # Will be set by get_total_frames
                fps=fps,
                x_original=x_original,
                y_original=y_original,
                z_original=z_original,
                scatter=scatter,
                ax=ax,
                audio_features=audio_features
            )
        
        # Get total frames from effect
        total_frames = effect_instance.get_total_frames()
        effect_instance.total_frames = total_frames  # Update instance
        
        # Calculate duration text
        duration_seconds = total_frames / fps
        if duration_seconds < 60:
            duration_text = f"{duration_seconds:.0f} seconds"
        else:
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            duration_text = f"{minutes}m {seconds}s"
        
        # Create update function that delegates to effect
        def update(frame):
            result = effect_instance.update(frame)
            return result
    
    print(f"Creating animation with {total_frames} frames ({duration_text} at {fps} fps)...")
    print("This may take several minutes depending on your system...")
    
    # Create progress bar (single line, auto-detect width)
    if tqdm:
        pbar = tqdm(total=total_frames, desc="Rendering video", unit="frame", ncols=None, leave=False)
        
        # Wrap update function to update progress bar
        original_update = update
        last_frame = [-1]  # Use list to allow modification in closure
        def update_with_progress(frame):
            result = original_update(frame)
            # Update progress bar to current frame (only if frame advanced)
            if frame > last_frame[0]:
                pbar.n = frame + 1  # tqdm uses 1-based indexing
                pbar.refresh()
                last_frame[0] = frame
            return result
        
        update_func = update_with_progress
    else:
        pbar = None
        update_func = update
    
    # Create animation
    anim = FuncAnimation(fig, update_func, frames=total_frames, 
                        interval=1000/fps, blit=False)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save animation
    if pbar:
        pbar.set_description("Saving video file")
    else:
        print(f"Saving animation to {output_path}...")
    writer = FFMpegWriter(fps=fps, bitrate=bitrate)
    anim.save(output_path, writer=writer)
    
    # Close progress bar
    if pbar:
        pbar.close()
    
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
  H8 - Heart Genesis with Music Sync: Creation story with BPM-synchronized beats (100 seconds)
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
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H8sync', 'H8sync3min', 'H9', 'H10'],
        default='A',
        help='Animation effect: A (multi-axis), B (camera orbit), C (combined), D (custom), E (heartbeat), F (spiral), G (figure-8), G1 (journey 90s), G2 (epic story 137s), H1 (genesis 100s), H2 (time reversal 90s), H3 (fractal 90s), H4 (dual hearts 120s), H5 (kaleidoscope 60s), H6 (nebula 120s), H7 (hologram 90s), H8 (genesis with music sync 100s), H8sync (genesis with real audio sync 100s), H8sync3min (extended 3.5min version 210s), H9 (Cuba to New Orleans musical journey ~698s), H10 (The Mission - Gabriel\'s Oboe spiritual journey) (default: A)'
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

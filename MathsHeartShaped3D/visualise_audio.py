"""
Visualise Audio Script
Creates heart animations from audio files with intelligent effect selection.
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

try:
    import librosa
except ImportError:
    print("Error: librosa is not installed. Please install it with:")
    print("  pip install librosa")
    sys.exit(1)

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def get_audio_duration(audio_path):
    """Get duration of audio file in seconds."""
    try:
        y, sr = librosa.load(audio_path, sr=22050)
        duration = librosa.get_duration(y=y, sr=sr)
        return float(duration)
    except Exception as e:
        raise ValueError(f"Failed to load audio file {audio_path}: {e}")


def auto_select_effect(duration, has_audio_features=False, skip_analysis=False):
    """
    Auto-select effect based on audio duration and characteristics.
    
    Parameters:
    - duration: Audio duration in seconds
    - has_audio_features: Whether audio analysis was successful
    - skip_analysis: Whether to skip analysis (use simple effects)
    
    Returns:
    - Effect name string
    """
    if skip_analysis or not has_audio_features:
        # Fallback to simple effects
        if duration < 30:
            return 'A'  # or 'B'
        elif duration < 60:
            return 'C'  # or 'D'
        elif duration < 120:
            return 'G1'  # or 'H1'
        else:
            return 'G2'  # or 'H4'
    else:
        # Audio-synchronized effects
        if duration < 30:
            return 'H8sync'
        elif duration < 120:  # 2 minutes
            return 'H8sync'
        elif duration < 300:  # 5 minutes
            return 'H8sync3min'
        else:
            # Long audio: choose H9 or H10 based on characteristics
            # For now, default to H9 for very long audio
            return 'H9'


def analyze_audio_file(audio_path, output_json_path=None, quiet=False):
    """
    Run audio analysis using analyze_audio.py
    
    Parameters:
    - audio_path: Path to audio file
    - output_json_path: Optional path for output JSON
    - quiet: Suppress output
    
    Returns:
    - Path to features JSON file, or None if analysis failed
    """
    try:
        # Import analyze_audio function
        from analyze_audio import analyze_audio
        
        if output_json_path is None:
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_json_path = os.path.join(
                tempfile.gettempdir(),
                f"{base_name}_features_{os.getpid()}.json"
            )
        
        if not quiet:
            print(f"Analyzing audio: {os.path.basename(audio_path)}...")
        
        features = analyze_audio(audio_path, output_json_path)
        
        if not quiet:
            print(f"Analysis complete: {os.path.basename(output_json_path)}")
        
        return output_json_path
    except Exception as e:
        if not quiet:
            print(f"Warning: Audio analysis failed: {e}")
        return None


def generate_video(effect, resolution, density, fps, bitrate, output_path,
                   audio_features_path=None, duration=None, quiet=False):
    """
    Generate video using heart_animation.py
    
    Parameters:
    - effect: Effect name
    - resolution: Video resolution
    - density: Point density
    - fps: Frame rate
    - bitrate: Video bitrate
    - output_path: Output video path
    - audio_features_path: Optional path to audio features JSON
    - duration: Optional duration override (not used, effect determines duration)
    - quiet: Suppress output
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        cmd = [
            sys.executable,
            'heart_animation.py',
            '--effect', effect,
            '--resolution', resolution,
            '--density', density,
            '--fps', str(fps),
            '--bitrate', str(bitrate),
            '--output', output_path
        ]
        
        if audio_features_path:
            cmd.extend(['--audio-features', audio_features_path])
        
        if quiet:
            # Suppress output
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return False
        else:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                return False
        
        return True
    except Exception as e:
        print(f"Error generating video: {e}")
        return False


def trim_video_to_duration(video_path, target_duration, output_path, quiet=False):
    """
    Trim or loop video to match target duration using ffmpeg.
    
    Parameters:
    - video_path: Path to input video file
    - target_duration: Target duration in seconds
    - output_path: Output path for trimmed video
    - quiet: Suppress output
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        # Check if ffprobe is available
        try:
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: ffprobe is not installed or not in PATH.")
            print("Please install ffmpeg (which includes ffprobe): https://ffmpeg.org/download.html")
            return False
        
        # Get video duration
        cmd_probe = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        
        result = subprocess.run(cmd_probe, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error getting video duration: {result.stderr}")
            return False
        
        try:
            video_duration = float(result.stdout.strip())
        except ValueError:
            print("Error: Could not parse video duration")
            return False
        
        if abs(video_duration - target_duration) < 0.1:
            # Durations match closely, just copy
            if video_path != output_path:
                shutil.copy2(video_path, output_path)
            return True
        
        if video_duration < target_duration:
            # Video is shorter: loop it
            loops_needed = int(target_duration / video_duration) + 1
            cmd = [
                'ffmpeg',
                '-stream_loop', str(loops_needed),
                '-i', video_path,
                '-t', str(target_duration),
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-y',
                output_path
            ]
        else:
            # Video is longer: trim it
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-t', str(target_duration),
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-y',
                output_path
            ]
        
        if quiet:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Error trimming video: {result.stderr}")
                return False
        else:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                return False
        
        return True
    except Exception as e:
        print(f"Error trimming video: {e}")
        return False


def combine_audio_video(video_path, audio_path, output_path, quiet=False):
    """
    Combine video with audio using ffmpeg.
    
    Parameters:
    - video_path: Path to video file
    - audio_path: Path to audio file
    - output_path: Output path for combined file
    - quiet: Suppress output
    
    Returns:
    - True if successful, False otherwise
    """
    try:
        # Check if ffmpeg is available
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Error: ffmpeg is not installed or not in PATH.")
            print("Please install ffmpeg: https://ffmpeg.org/download.html")
            return False
        
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            '-y',  # Overwrite output file
            output_path
        ]
        
        if quiet:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return False
        else:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                return False
        
        return True
    except Exception as e:
        print(f"Error combining audio and video: {e}")
        return False


def get_output_path(input_path, custom_output=None, overwrite=False):
    """
    Determine output path for video file.
    
    Parameters:
    - input_path: Input audio file path
    - custom_output: Custom output path (optional)
    - overwrite: Whether to overwrite existing files
    
    Returns:
    - Output path string
    """
    if custom_output:
        output_path = custom_output
    else:
        # Use same directory and name as input, but with .mp4 extension
        base_path = Path(input_path)
        output_path = str(base_path.with_suffix('.mp4'))
    
    # Handle existing file
    if os.path.exists(output_path) and not overwrite:
        # Add timestamp
        base_path = Path(output_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = base_path.stem
        suffix = base_path.suffix
        output_path = str(base_path.parent / f"{stem}_{timestamp}{suffix}")
    
    return output_path


def process_single_file(audio_path, args):
    """Process a single audio file."""
    if not os.path.exists(audio_path):
        print(f"Warning: Audio file not found: {audio_path}")
        return False
    
    try:
        # Get audio duration
        if not args.quiet:
            print(f"\nProcessing: {os.path.basename(audio_path)}")
        
        original_duration = get_audio_duration(audio_path)
        duration = original_duration
        
        # Handle duration constraints
        audio_needs_looping = False
        if duration < 10:
            if not args.quiet:
                print(f"Warning: Audio too short ({duration:.1f}s), will loop to reach minimum 10s")
            audio_needs_looping = True
            duration = max(duration, 10)
        elif duration > 1200:  # 20 minutes
            if not args.quiet:
                print(f"Warning: Audio too long ({duration:.1f}s), will trim to 20 minutes")
            duration = 1200
        
        if not args.quiet:
            print(f"Duration: {duration:.2f} seconds")
        
        # Determine effect
        if args.effect == 'auto-select':
            # Run audio analysis if needed
            audio_features_path = None
            has_audio_features = False
            
            if not args.skip_analysis:
                audio_features_path = analyze_audio_file(audio_path, quiet=args.quiet)
                has_audio_features = audio_features_path is not None
            
            effect = auto_select_effect(duration, has_audio_features, args.skip_analysis)
        else:
            effect = args.effect
            # Check if effect requires audio features
            audio_sync_effects = ['H8sync', 'H8sync3min', 'H9', 'H10']
            audio_features_path = None
            
            if effect in audio_sync_effects and not args.skip_analysis:
                audio_features_path = analyze_audio_file(audio_path, quiet=args.quiet)
                if not audio_features_path:
                    if not args.quiet:
                        print(f"Warning: Audio analysis failed, effect {effect} may not work properly")
        
        if not args.quiet:
            print(f"Selected effect: {effect}")
        
        # Determine output path
        output_path = get_output_path(audio_path, args.output, args.overwrite)
        
        # Generate video (effect will have its own duration)
        temp_video = output_path + '.temp.mp4'
        if not args.quiet:
            print(f"Generating video: {os.path.basename(output_path)}")
        
        success = generate_video(
            effect=effect,
            resolution=args.resolution,
            density=args.density,
            fps=args.fps,
            bitrate=args.bitrate,
            output_path=temp_video,
            audio_features_path=audio_features_path,
            duration=None,  # Effect determines its own duration
            quiet=args.quiet
        )
        
        if not success:
            print(f"Error: Video generation failed for {audio_path}")
            return False
        
        # Trim/loop video to match audio duration exactly
        if not args.quiet:
            print(f"Adjusting video duration to match audio ({duration:.2f}s)...")
        
        trimmed_video = output_path + '.trimmed.mp4'
        success = trim_video_to_duration(temp_video, duration, trimmed_video, quiet=args.quiet)
        
        if not success:
            print(f"Error: Failed to adjust video duration")
            if os.path.exists(temp_video):
                os.remove(temp_video)
            return False
        
        # Handle audio looping/trimming if needed
        audio_to_use = audio_path
        temp_audio = None
        
        if original_duration < 10:
            # Loop audio to reach minimum duration
            temp_audio = output_path + '.looped_audio.mp3'
            if not args.quiet:
                print(f"Looping audio to {duration:.1f}s...")
            
            loops_needed = int(duration / original_duration) + 1
            cmd = [
                'ffmpeg',
                '-stream_loop', str(loops_needed),
                '-i', audio_path,
                '-t', str(duration),
                '-c:a', 'aac',
                '-y',
                temp_audio
            ]
            
            if args.quiet:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Error looping audio: {result.stderr}")
                    if os.path.exists(temp_video):
                        os.remove(temp_video)
                    if os.path.exists(trimmed_video):
                        os.remove(trimmed_video)
                    return False
            else:
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print("Error: Failed to loop audio")
                    if os.path.exists(temp_video):
                        os.remove(temp_video)
                    if os.path.exists(trimmed_video):
                        os.remove(trimmed_video)
                    return False
            
            audio_to_use = temp_audio
        elif original_duration > 1200:
            # Trim audio to 20 minutes
            temp_audio = output_path + '.trimmed_audio.mp3'
            if not args.quiet:
                print(f"Trimming audio to {duration:.1f}s...")
            
            cmd = [
                'ffmpeg',
                '-i', audio_path,
                '-t', str(duration),
                '-c:a', 'copy',
                '-y',
                temp_audio
            ]
            
            if args.quiet:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Error trimming audio: {result.stderr}")
                    if os.path.exists(temp_video):
                        os.remove(temp_video)
                    if os.path.exists(trimmed_video):
                        os.remove(trimmed_video)
                    return False
            else:
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print("Error: Failed to trim audio")
                    if os.path.exists(temp_video):
                        os.remove(temp_video)
                    if os.path.exists(trimmed_video):
                        os.remove(trimmed_video)
                    return False
            
            audio_to_use = temp_audio
        
        # Combine with audio
        if not args.quiet:
            print(f"Combining with audio...")
        
        # Create final output path (with audio)
        final_output = output_path
        if not final_output.endswith('.mp4'):
            final_output += '.mp4'
        
        success = combine_audio_video(trimmed_video, audio_to_use, final_output, quiet=args.quiet)
        
        # Clean up temp audio file
        if temp_audio and os.path.exists(temp_audio):
            os.remove(temp_audio)
        
        # Clean up temp files
        if os.path.exists(temp_video):
            os.remove(temp_video)
        if os.path.exists(trimmed_video):
            os.remove(trimmed_video)
        
        if not success:
            print(f"Error: Failed to combine audio with video for {audio_path}")
            return False
        
        if not args.quiet:
            print(f"Success! Output: {final_output}")
        
        # Clean up temporary features file
        if audio_features_path and os.path.exists(audio_features_path):
            try:
                os.remove(audio_features_path)
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        import traceback
        traceback.print_exc()
        return False


def process_multiple_files(audio_paths, args):
    """Process multiple audio files and combine them."""
    if not audio_paths:
        return False
    
    # Validate all files exist
    valid_files = []
    for path in audio_paths:
        if os.path.exists(path):
            valid_files.append(path)
        else:
            print(f"Warning: Audio file not found: {path}")
    
    if not valid_files:
        print("Error: No valid audio files to process")
        return False
    
    try:
        # Get durations for all files
        durations = []
        total_duration = 0
        
        if not args.quiet:
            print(f"\nProcessing {len(valid_files)} audio file(s)...")
        
        for path in valid_files:
            try:
                duration = get_audio_duration(path)
                durations.append((path, duration))
                total_duration += duration
                if not args.quiet:
                    print(f"  {os.path.basename(path)}: {duration:.2f}s")
            except Exception as e:
                print(f"Warning: Failed to get duration for {path}: {e}")
                continue
        
        if not durations:
            print("Error: No valid audio files with readable durations")
            return False
        
        # Add transition time (1 second fade between files)
        transition_time = (len(durations) - 1) * 1.0
        total_duration += transition_time
        
        if not args.quiet:
            print(f"Total duration: {total_duration:.2f}s (including transitions)")
        
        # Determine effect based on total duration
        if args.effect == 'auto-select':
            # For multiple files, we'll use a simple approach
            # Analyze first file to see if we can get features
            audio_features_path = None
            has_audio_features = False
            
            if not args.skip_analysis and durations:
                audio_features_path = analyze_audio_file(durations[0][0], quiet=args.quiet)
                has_audio_features = audio_features_path is not None
            
            effect = auto_select_effect(total_duration, has_audio_features, args.skip_analysis)
        else:
            effect = args.effect
            audio_features_path = None
            
            if effect in ['H8sync', 'H8sync3min', 'H9', 'H10'] and not args.skip_analysis and durations:
                audio_features_path = analyze_audio_file(durations[0][0], quiet=args.quiet)
        
        if not args.quiet:
            print(f"Selected effect: {effect}")
        
        # Determine output path (use first file's name)
        first_file = valid_files[0]
        output_path = get_output_path(first_file, args.output, args.overwrite)
        
        # For multiple files, we need to:
        # 1. Generate individual videos (or one long video)
        # 2. Combine audio files with transitions
        # 3. Combine video with combined audio
        
        # For now, we'll generate one video for the total duration
        # and combine all audio files first
        
        # Combine audio files with ffmpeg (with fade transitions)
        combined_audio = output_path + '.combined_audio.mp3'
        
        if not args.quiet:
            print("Combining audio files with transitions...")
        
        # Simple approach: concatenate with fades
        # For each file, add fade in/out, then concatenate
        filter_parts = []
        inputs = []
        
        for i, (path, dur) in enumerate(durations):
            inputs.extend(['-i', path])
            
            if i == 0:
                # First file: fade in at start, fade out at end (1s before end)
                fade_out_start = max(0, dur - 1)
                if dur > 1:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1[a{i}]")
                else:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d={dur}[a{i}]")
            elif i == len(durations) - 1:
                # Last file: fade in at start, fade out at end
                fade_out_start = max(0, dur - 1)
                if dur > 1:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1[a{i}]")
                else:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d={dur},afade=t=out:st=0:d={dur}[a{i}]")
            else:
                # Middle files: fade in and fade out
                fade_out_start = max(0, dur - 1)
                if dur > 2:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d=1,afade=t=out:st={fade_out_start}:d=1[a{i}]")
                elif dur > 1:
                    filter_parts.append(f"[{i}:a]afade=t=in:st=0:d=0.5,afade=t=out:st={dur-0.5}:d=0.5[a{i}]")
                else:
                    filter_parts.append(f"[{i}:a]volume=0.5[a{i}]")
        
        # Concatenate all processed audio streams
        concat_inputs = ''.join([f"[a{i}]" for i in range(len(durations))])
        filter_complex = ';'.join(filter_parts) + f";{concat_inputs}concat=n={len(durations)}:v=0:a=1[outa]"
        
        cmd = ['ffmpeg'] + inputs + [
            '-filter_complex', filter_complex,
            '-map', '[outa]',
            '-y',
            combined_audio
        ]
        
        if args.quiet:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error combining audio: {result.stderr}")
                return False
        else:
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print("Error: Failed to combine audio files")
                return False
        
        # Generate video (effect will have its own duration)
        temp_video = output_path + '.temp.mp4'
        if not args.quiet:
            print(f"Generating video: {os.path.basename(output_path)}")
        
        success = generate_video(
            effect=effect,
            resolution=args.resolution,
            density=args.density,
            fps=args.fps,
            bitrate=args.bitrate,
            output_path=temp_video,
            audio_features_path=audio_features_path,
            duration=None,  # Effect determines its own duration
            quiet=args.quiet
        )
        
        if not success:
            print("Error: Video generation failed")
            if os.path.exists(combined_audio):
                os.remove(combined_audio)
            return False
        
        # Trim/loop video to match combined audio duration exactly
        if not args.quiet:
            print(f"Adjusting video duration to match audio ({total_duration:.2f}s)...")
        
        trimmed_video = output_path + '.trimmed.mp4'
        success = trim_video_to_duration(temp_video, total_duration, trimmed_video, quiet=args.quiet)
        
        if not success:
            print("Error: Failed to adjust video duration")
            if os.path.exists(temp_video):
                os.remove(temp_video)
            if os.path.exists(combined_audio):
                os.remove(combined_audio)
            return False
        
        # Combine video with combined audio
        if not args.quiet:
            print("Combining video with audio...")
        
        final_output = output_path
        success = combine_audio_video(trimmed_video, combined_audio, final_output, quiet=args.quiet)
        
        # Clean up temp files
        if os.path.exists(temp_video):
            os.remove(temp_video)
        if os.path.exists(trimmed_video):
            os.remove(trimmed_video)
        if os.path.exists(combined_audio):
            os.remove(combined_audio)
        
        if not success:
            print("Error: Failed to combine video with audio")
            return False
        
        if not args.quiet:
            print(f"Success! Output: {final_output}")
        
        # Clean up temporary features file
        if audio_features_path and os.path.exists(audio_features_path):
            try:
                os.remove(audio_features_path)
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"Error processing multiple files: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Create heart animations from audio files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (single file, auto-select effect)
  python visualise_audio.py song.mp3

  # High-quality with specific effect
  python visualise_audio.py song.mp3 --resolution large --effect H8sync

  # Multiple files combined
  python visualise_audio.py track1.mp3 track2.mp3 track3.mp3

  # Custom output path
  python visualise_audio.py song.mp3 --output /path/to/output.mp4

  # Skip audio analysis (faster, simpler effects)
  python visualise_audio.py song.mp3 --skip-analysis

  # Overwrite existing files
  python visualise_audio.py song.mp3 --overwrite
        """
    )
    
    parser.add_argument(
        'audio_files',
        nargs='+',
        help='Audio file(s) to process (MP3, WAV, M4A, FLAC, etc.)'
    )
    
    parser.add_argument(
        '--resolution', '-r',
        choices=['small', 'medium', 'large', '4k'],
        default='large',
        help='Video resolution (default: large)'
    )
    
    parser.add_argument(
        '--density', '-d',
        choices=['lower', 'low', 'medium', 'high'],
        default='lower',
        help='Point density (default: lower)'
    )
    
    parser.add_argument(
        '--effect', '-e',
        default='auto-select',
        help='Effect selection: auto-select or specific effect name (A, B, C, D, E, F, G, G1, G2, H1-H10, H8sync, H8sync3min) (default: auto-select)'
    )
    
    parser.add_argument(
        '--bitrate', '-b',
        type=int,
        default=5000,
        help='Video bitrate in kbps (default: 5000)'
    )
    
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frame rate (default: 30)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Custom output path (for single file or combined)'
    )
    
    parser.add_argument(
        '--combine',
        action='store_true',
        help='Combine multiple files into one video (default behavior)'
    )
    
    parser.add_argument(
        '--skip-analysis',
        action='store_true',
        help='Skip audio feature analysis (use simple effects that don\'t require analysis)'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files (default: rename with timestamp)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress progress output'
    )
    
    args = parser.parse_args()
    
    # Process files
    if len(args.audio_files) == 1:
        success = process_single_file(args.audio_files[0], args)
    else:
        success = process_multiple_files(args.audio_files, args)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())


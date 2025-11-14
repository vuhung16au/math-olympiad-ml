"""
Audio Feature Extraction Tool
Analyzes audio files to extract beats, tempo, onsets, loudness, and bass information
for synchronization with heart animations.
"""

import librosa
import numpy as np
import json
import os
import sys
import argparse


def analyze_audio(audio_path, output_json_path=None):
    """
    Analyze audio file and extract beats, tempo, onsets, loudness, bass.
    Save results to JSON for animation to use.
    
    Parameters:
    - audio_path: Path to audio file (MP3, WAV, etc.)
    - output_json_path: Optional path for output JSON. If None, uses audio filename.
    
    Returns:
    - Dictionary containing all extracted features
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Analyzing audio: {audio_path}")
    
    # Load audio (use lower sample rate for speed)
    print("Loading audio file...")
    y, sr = librosa.load(audio_path, sr=22050)
    duration = librosa.get_duration(y=y, sr=sr)
    
    print(f"Audio duration: {duration:.2f} seconds")
    print(f"Sample rate: {sr} Hz")
    
    # 1. Detect beats and tempo
    print("Detecting beats and tempo...")
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # Convert tempo to float (handle numpy array)
    if hasattr(tempo, '__iter__') and not isinstance(tempo, str):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
    else:
        tempo = float(tempo)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    print(f"  Detected tempo: {tempo:.1f} BPM")
    print(f"  Found {len(beat_times)} beats")
    
    # 2. Detect onsets (new sound events)
    print("Detecting onsets...")
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='frames')
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    print(f"  Found {len(onset_times)} onsets")
    
    # 3. Calculate RMS energy (loudness) over time
    print("Calculating loudness (RMS energy)...")
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.frames_to_time(range(len(rms)), sr=sr)
    
    # Normalize RMS to 0-1 range
    rms_min = rms.min()
    rms_max = rms.max()
    rms_range = rms_max - rms_min
    if rms_range > 1e-6:
        rms_normalized = (rms - rms_min) / rms_range
    else:
        rms_normalized = np.ones_like(rms) * 0.5  # Default to middle if no variation
    
    print(f"  RMS range: {rms_min:.4f} to {rms_max:.4f}")
    
    # 4. Calculate spectral centroid (brightness) - inverse = bass
    print("Calculating bass strength...")
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spec_times = librosa.frames_to_time(range(len(spec_cent)), sr=sr)
    
    # Normalize and invert for bass (low centroid = more bass)
    spec_min = spec_cent.min()
    spec_max = spec_cent.max()
    spec_range = spec_max - spec_min
    if spec_range > 1e-6:
        spec_normalized = (spec_cent - spec_min) / spec_range
        bass_strength = 1.0 - spec_normalized  # Invert: low centroid = high bass
    else:
        bass_strength = np.ones_like(spec_cent) * 0.5  # Default to middle
    
    print(f"  Spectral centroid range: {spec_min:.1f} to {spec_max:.1f} Hz")
    
    # 5. Dynamic tempo tracking (tempo changes over time)
    print("Tracking dynamic tempo changes...")
    tempo_times = []
    tempo_values = []
    window_size = 3.0  # 3 second windows
    hop_size = 0.5    # Check every 0.5 seconds
    
    for t in np.arange(0, duration, hop_size):
        start_frame = librosa.time_to_frames(t, sr=sr)
        end_frame = librosa.time_to_frames(min(t + window_size, duration), sr=sr)
        
        if end_frame > start_frame and end_frame <= len(y):
            y_segment = y[start_frame:end_frame]
            if len(y_segment) > 0:
                try:
                    tempo_local, _ = librosa.beat.beat_track(y=y_segment, sr=sr)
                    # Convert tempo_local to float (handle numpy array)
                    if hasattr(tempo_local, '__iter__') and not isinstance(tempo_local, str):
                        tempo_local = float(tempo_local[0]) if len(tempo_local) > 0 else tempo
                    else:
                        tempo_local = float(tempo_local)
                    tempo_times.append(t)
                    tempo_values.append(tempo_local)
                except:
                    # If beat tracking fails for segment, use global tempo
                    tempo_times.append(t)
                    tempo_values.append(tempo)
    
    print(f"  Tracked tempo at {len(tempo_times)} time points")
    
    # 6. Calculate zero-crossing rate (for detecting silence/activity)
    print("Calculating zero-crossing rate...")
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    zcr_times = librosa.frames_to_time(range(len(zcr)), sr=sr)
    zcr_normalized = (zcr - zcr.min()) / (zcr.max() - zcr.min() + 1e-6)
    
    # Save all features to JSON
    features = {
        'audio_file': os.path.basename(audio_path),
        'duration': float(duration),
        'sample_rate': int(sr),
        'tempo_global': float(tempo),
        'beat_times': [float(t) for t in beat_times],
        'onset_times': [float(t) for t in onset_times],
        'rms_times': [float(t) for t in rms_times],
        'rms_values': [float(v) for v in rms_normalized],
        'bass_times': [float(t) for t in spec_times],
        'bass_values': [float(v) for v in bass_strength],
        'tempo_times': tempo_times,
        'tempo_values': tempo_values,
        'zcr_times': [float(t) for t in zcr_times],
        'zcr_values': [float(v) for v in zcr_normalized]
    }
    
    # Determine output path
    if output_json_path is None:
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_json_path = f"{base_name}_features.json"
    
    # Save to JSON
    with open(output_json_path, 'w') as f:
        json.dump(features, f, indent=2)
    
    print(f"\nAnalysis complete!")
    print(f"  Saved to: {output_json_path}")
    print(f"\nSummary:")
    print(f"  - {len(beat_times)} beats detected")
    print(f"  - {len(onset_times)} onsets detected")
    print(f"  - {len(rms_times)} RMS energy points")
    print(f"  - {len(tempo_times)} tempo measurements")
    print(f"  - Global tempo: {tempo:.1f} BPM")
    
    return features


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Analyze audio file and extract features for animation synchronization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_audio.py inputs/H8InfiniteStars2.mp3
  python analyze_audio.py inputs/H8InfiniteStars2.mp3 -o audio_features.json
  python analyze_audio.py Engima.mp3 --output my_features.json
        """
    )
    
    parser.add_argument(
        'audio_file',
        help='Path to audio file (MP3, WAV, etc.)'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_json',
        help='Output JSON file path (default: {audio_filename}_features.json)'
    )
    
    args = parser.parse_args()
    
    try:
        features = analyze_audio(args.audio_file, args.output_json)
        print("\nSuccess! You can now use this JSON file with heart_animation.py")
        print(f"  Example: python heart_animation.py --effect H8sync --audio-features {args.output_json or os.path.splitext(os.path.basename(args.audio_file))[0] + '_features.json'}")
        return 0
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())


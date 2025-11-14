# Audio Analysis Tool

## Overview

The `analyze_audio.py` tool extracts musical features from audio files to enable synchronization between heart animations and music. It uses **librosa** (a powerful Music Information Retrieval library) to detect beats, tempo, onsets, loudness, and bass information.

## Features Extracted

The tool analyzes audio files and extracts the following features:

1. **Beats**: Precise timestamps of each beat in the music
2. **Tempo**: Global BPM and dynamic tempo changes over time
3. **Onsets**: Moments where new sounds begin (transitions from silence to sound)
4. **Loudness (RMS Energy)**: Normalized energy levels (0-1) over time
5. **Bass Strength**: Low-frequency energy levels (inverted spectral centroid)
6. **Zero-Crossing Rate**: Activity/silence detection

## Installation

Ensure you have `librosa` installed:

```powershell
uv pip install librosa
```

Or install all requirements:

```powershell
uv pip install -r requirements.txt
```

## Usage

### Basic Usage

Analyze an audio file (output will be `{filename}_features.json`):

```powershell
python analyze_audio.py inputs/H8InfiniteStars2.mp3
```

This creates `H8InfiniteStars2_features.json` in the current directory.

### Custom Output Path

Specify a custom output file:

```powershell
python analyze_audio.py inputs/H8InfiniteStars2.mp3 -o audio_features.json
```

Or:

```powershell
python analyze_audio.py inputs/H8InfiniteStars2.mp3 --output my_audio_features.json
```

## Output Format

The tool generates a JSON file with the following structure:

```json
{
  "audio_file": "H8InfiniteStars2.mp3",
  "duration": 100.5,
  "sample_rate": 22050,
  "tempo_global": 75.2,
  "beat_times": [0.5, 1.2, 1.8, 2.4, ...],
  "onset_times": [0.1, 0.8, 1.5, 2.1, ...],
  "rms_times": [0.0, 0.023, 0.046, ...],
  "rms_values": [0.2, 0.5, 0.8, 0.3, ...],
  "bass_times": [0.0, 0.023, 0.046, ...],
  "bass_values": [0.6, 0.4, 0.7, 0.5, ...],
  "tempo_times": [0.0, 0.5, 1.0, 1.5, ...],
  "tempo_values": [75.0, 76.2, 75.8, ...],
  "zcr_times": [0.0, 0.023, 0.046, ...],
  "zcr_values": [0.1, 0.3, 0.2, ...]
}
```

### Field Descriptions

- **audio_file**: Original audio filename
- **duration**: Total duration in seconds
- **sample_rate**: Audio sample rate used for analysis
- **tempo_global**: Overall BPM of the track
- **beat_times**: Array of beat timestamps (seconds)
- **onset_times**: Array of onset timestamps (seconds)
- **rms_times**: Time points for RMS energy measurements
- **rms_values**: Normalized loudness values (0-1, where 1 = loudest)
- **bass_times**: Time points for bass measurements
- **bass_values**: Normalized bass strength (0-1, where 1 = most bass)
- **tempo_times**: Time points for dynamic tempo tracking
- **tempo_values**: BPM values at each time point
- **zcr_times**: Time points for zero-crossing rate
- **zcr_values**: Normalized activity levels (0-1)

## Workflow

### Step 1: Analyze Audio

```powershell
python analyze_audio.py inputs/H8InfiniteStars2.mp3
```

Output: `H8InfiniteStars2_features.json`

### Step 2: Use with Animation

```powershell
python heart_animation.py --effect H8sync --audio-features H8InfiniteStars2_features.json
```

## Sample Commands

### Analyze Different Audio Formats

```powershell
# MP3 file
python analyze_audio.py inputs/H8InfiniteStars2.mp3

# WAV file
python analyze_audio.py audio.wav

# With custom output
python analyze_audio.py Engima.mp3 -o enigma_features.json
```

### Complete Workflow Example

```powershell
# 1. Analyze audio
python analyze_audio.py inputs/H8InfiniteStars2.mp3

# 2. Generate animation with audio sync
python heart_animation.py --effect H8sync --audio-features H8InfiniteStars2_features.json --output outputs/heart_synced.mp4

# 3. Combine with original audio (if needed)
ffmpeg -i outputs/heart_synced.mp4 -i inputs/H8InfiniteStars2.mp3 -c:v copy -c:a aac -b:a 192k outputs/heart_with_audio.mp4
```

## Performance

- **Analysis Time**: Typically 5-30 seconds depending on audio length
- **Sample Rate**: Uses 22050 Hz (lower than original) for faster processing
- **Memory**: Low memory footprint, suitable for most audio files

## Troubleshooting

### librosa Not Found

```powershell
# Install librosa
uv pip install librosa
```

### Audio File Not Found

```
FileNotFoundError: Audio file not found: inputs/H8InfiniteStars2.mp3
```

**Solution**: Check the file path and ensure the audio file exists.

### Analysis Takes Too Long

For very long audio files (>10 minutes), consider trimming first:

```powershell
# Trim to first 100 seconds
ffmpeg -i long_audio.mp3 -t 100 -c copy short_audio.mp3

# Then analyze
python analyze_audio.py short_audio.mp3
```

## Integration with Animation

The extracted features are used by the `H8sync` effect in `heart_animation.py` to:

- **Sync heartbeat pulses** with detected beats
- **Adjust rotation speed** based on tempo
- **Modify zoom** based on loudness
- **Change brightness** based on bass
- **Trigger effects** on onsets

See `docs/effects.md` for details on the H8sync effect.

## Technical Details

### Beat Detection

Uses librosa's `beat_track()` function which:
- Estimates tempo using autocorrelation
- Tracks beats using dynamic programming
- Provides precise beat timestamps

### Onset Detection

Uses librosa's `onset_detect()` which:
- Detects sudden changes in spectral content
- Identifies note onsets and transients
- Useful for detecting musical events

### RMS Energy

- Calculated over short time windows (~23ms at 22050 Hz)
- Normalized to 0-1 range for easy use in animation
- Higher values = louder sections

### Bass Strength

- Derived from spectral centroid (brightness measure)
- Inverted so low centroid = high bass
- Normalized to 0-1 range

### Dynamic Tempo

- Analyzes tempo in 3-second windows
- Updates every 0.5 seconds
- Tracks tempo changes throughout the song

## Related Files

- **Main Script**: `analyze_audio.py`
- **Animation Script**: `heart_animation.py`
- **Effect Documentation**: `docs/effects.md`
- **Build Script**: `scripts/build_h8sync_large.ps1`

---

**Last Updated**: November 2025  
**Version**: 1.0


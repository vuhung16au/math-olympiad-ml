# Visualise Audio Script Documentation

## Overview

The `visualise_audio.py` script simplifies the video creation process by automatically generating heart animations from audio files. It intelligently selects appropriate animation effects based on audio characteristics, handles multiple files, and provides a streamlined workflow from audio input to final video output.

### Key Features

- **Automatic Effect Selection**: Intelligently chooses the best animation effect based on audio duration and characteristics
- **Audio Synchronization**: Automatically analyzes audio features (beats, tempo, loudness) for synchronized effects
- **Multiple File Support**: Combine multiple audio files into a single video with smooth transitions
- **Flexible Configuration**: Customize resolution, density, bitrate, and other parameters
- **Robust Error Handling**: Gracefully handles corrupted files, missing dependencies, and edge cases
- **Progress Tracking**: Real-time progress indication with ETA for long operations

### Workflow

1. **Audio Analysis**: Analyzes audio file to extract features (beats, tempo, loudness, bass, onsets)
2. **Effect Selection**: Automatically selects appropriate effect or uses user-specified effect
3. **Video Generation**: Creates heart animation synchronized with audio
4. **Audio Combination**: Combines video with original audio using ffmpeg

## Sample Commands (Example Runs)

### Basic Usage

```bash
# Single audio file with automatic effect selection
python visualise_audio.py song.mp3

# Output: song.mp4 (in same folder as song.mp3)
# Effect: Auto-selected based on audio duration and characteristics
# Resolution: large (1920x1080)
# Density: lower (~5,000 points)
```

### High-Quality Output

```bash
# Full HD with specific effect
python visualise_audio.py song.mp3 --resolution large --effect H8sync --density medium

# 4K output for maximum quality
python visualise_audio.py song.mp3 --resolution 4k --bitrate 20000 --density low
```

### Multiple Files (Combined)

```bash
# Combine multiple audio files into one video
python visualise_audio.py track1.mp3 track2.mp3 track3.wav

# Output: track1.mp4 (uses first filename)
# Transitions: 1-second fade in/out between files
# Duration: Sum of all audio files + transition time
```

### Custom Output Path

```bash
# Specify custom output location
python visualise_audio.py song.mp3 --output /path/to/my_video.mp4

# Multiple files with custom output
python visualise_audio.py file1.mp3 file2.mp3 --output combined_playlist.mp4
```

### Fast Processing (Skip Analysis)

```bash
# Skip audio analysis for faster processing (uses simple effects)
python visualise_audio.py song.mp3 --skip-analysis

# Useful for quick previews or when audio sync is not needed
```

### Overwrite Existing Files

```bash
# Overwrite existing output file
python visualise_audio.py song.mp3 --overwrite

# Without --overwrite: Automatically renames with timestamp
# Example: song.mp3 → song_20240101_120000.mp4
```

### Quiet Mode

```bash
# Suppress progress output (useful for batch processing)
python visualise_audio.py song.mp3 --quiet
```

### Different Resolutions

```bash
# Small resolution (640x480) - fastest
python visualise_audio.py song.mp3 --resolution small

# Medium resolution (1280x720) - balanced
python visualise_audio.py song.mp3 --resolution medium

# Large resolution (1920x1080) - default, high quality
python visualise_audio.py song.mp3 --resolution large

# 4K resolution (3840x2160) - maximum quality
python visualise_audio.py song.mp3 --resolution 4k
```

### Different Densities

```bash
# Lower density (~5,000 points) - fastest rendering
python visualise_audio.py song.mp3 --density lower

# Low density (~10,000 points) - good balance
python visualise_audio.py song.mp3 --density low

# Medium density (~22,500 points) - higher quality
python visualise_audio.py song.mp3 --density medium

# High density (~40,000 points) - maximum detail
python visualise_audio.py song.mp3 --density high
```

### Force Specific Effect

```bash
# Use specific effect instead of auto-selection
python visualise_audio.py song.mp3 --effect H8sync

# Simple effects (no audio analysis needed)
python visualise_audio.py song.mp3 --effect A
python visualise_audio.py song.mp3 --effect G1

# Epic effects
python visualise_audio.py song.mp3 --effect G2
python visualise_audio.py song.mp3 --effect H1
```

### Custom Bitrate and Frame Rate

```bash
# Custom bitrate (default: 5000 kbps)
python visualise_audio.py song.mp3 --bitrate 8000

# Custom frame rate (default: 30 fps)
python visualise_audio.py song.mp3 --fps 60
```

### Batch Processing Examples

```bash
# Process all MP3 files in current directory
python visualise_audio.py *.mp3

# Process files from different directories
python visualise_audio.py /path/to/song1.mp3 /path/to/song2.mp3

# Combine playlist with custom settings
python visualise_audio.py playlist/*.mp3 --resolution large --density lower --output playlist_combined.mp4
```

### Error Handling Examples

```bash
# If output file exists, it will be renamed automatically
python visualise_audio.py song.mp3
# If song.mp4 exists → song_20240101_120000.mp4

# Force overwrite
python visualise_audio.py song.mp3 --overwrite

# Corrupted files are skipped with warning
python visualise_audio.py good.mp3 corrupted.mp3 good2.mp3
# Output: Continues processing good files, skips corrupted.mp3 with warning
```

### Real-World Use Cases

```bash
# Quick preview (fast, lower quality)
python visualise_audio.py song.mp3 --resolution small --density lower --skip-analysis

# Social media post (medium quality, fast)
python visualise_audio.py song.mp3 --resolution medium --density lower

# YouTube video (high quality)
python visualise_audio.py song.mp3 --resolution large --density medium --effect H8sync

# Professional production (maximum quality)
python visualise_audio.py song.mp3 --resolution 4k --density low --bitrate 20000 --effect H9

# Music video playlist
python visualise_audio.py track1.mp3 track2.mp3 track3.mp3 --resolution large --output music_video.mp4
```

## Effect Selection Guide

When using `--effect auto-select` (default), the script chooses effects based on:

- **Audio Duration**: Shorter files get simpler effects, longer files get epic effects
- **Audio Characteristics**: Music gets synchronized effects (H8sync, H9, H10), ambient gets simple effects
- **Analysis Success**: If audio analysis fails, falls back to simple effects

### Recommended Effects by Use Case

- **Quick Demos**: `--effect A` or `--skip-analysis`
- **Music Videos**: `--effect auto-select` (uses H8sync/H9/H10)
- **Short Clips**: `--effect C` or `--effect D`
- **Epic Stories**: `--effect G2` or `--effect H1`
- **Classical Music**: `--effect H10`
- **Energetic Music**: `--effect H8sync` or `--effect H9`

## Technical Notes

- **Audio Formats**: Supports all formats readable by librosa (MP3, WAV, M4A, FLAC, etc.)
- **Video Format**: Always outputs MP4 (H.264 video, AAC audio)
- **Synchronization**: Audio and video are perfectly synchronized
- **Transitions**: 1-second fade in/out between multiple files
- **Minimum Duration**: Audio shorter than 10 seconds is looped
- **Maximum Duration**: Audio longer than 20 minutes is trimmed (with warning)

## Dependencies

- Python 3.12+
- numpy
- matplotlib
- librosa (for audio analysis)
- tqdm (for progress bars)
- ffmpeg (for audio/video combination)

Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Troubleshooting

### Audio Analysis Fails
- Use `--skip-analysis` to use simple effects
- Check audio file is not corrupted
- Ensure librosa is properly installed

### Output File Already Exists
- Use `--overwrite` to replace existing file
- Or let script auto-rename with timestamp

### Processing Too Slow
- Use `--resolution small` or `--density lower`
- Use `--skip-analysis` to skip audio analysis
- Process files individually instead of combining

### Missing Dependencies
- Install with: `uv pip install -r requirements.txt`
- Ensure ffmpeg is in PATH


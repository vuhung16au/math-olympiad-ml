# Heart Animation Tutorials

Quick command reference for all effects.

## Basic Effects (No Audio Required)

### A - Multi-Axis Rotation
```bash
python heart_animation.py --effect A --resolution large --output outputs/effect_a.mp4
```

### B - Camera Orbit
```bash
python heart_animation.py --effect B --resolution large --output outputs/effect_b.mp4
```

### C - Combined
```bash
python heart_animation.py --effect C --resolution large --output outputs/effect_c.mp4
```

### D - Custom
```bash
python heart_animation.py --effect D --resolution large --output outputs/effect_d.mp4
```

### E - Heartbeat Pulse
```bash
python heart_animation.py --effect E --resolution large --output outputs/effect_e.mp4
```

### F - Spiral Ascent
```bash
python heart_animation.py --effect F --resolution large --output outputs/effect_f.mp4
```

### G - Figure-8 Dance
```bash
python heart_animation.py --effect G --resolution large --output outputs/effect_g.mp4
```

### G1 - Heart Journey (90s)
```bash
python heart_animation.py --effect G1 --resolution large --density lower --output outputs/effect_g1.mp4
```

### G2 - Epic Story (137s)
```bash
python heart_animation.py --effect G2 --resolution large --density lower --output outputs/effect_g2.mp4
```

## H Series Effects (No Audio Required)

### H1 - Genesis (100s)
```bash
python heart_animation.py --effect H1 --resolution large --density lower --output outputs/effect_h1.mp4
```

### H2 - Time Reversal (90s)
```bash
python heart_animation.py --effect H2 --resolution large --density lower --output outputs/effect_h2.mp4
```

### H3 - Fractal (90s)
```bash
python heart_animation.py --effect H3 --resolution large --density lower --output outputs/effect_h3.mp4
```

### H4 - Dual Hearts (120s)
```bash
python heart_animation.py --effect H4 --resolution large --density lower --output outputs/effect_h4.mp4
```

### H5 - Kaleidoscope (60s)
```bash
python heart_animation.py --effect H5 --resolution large --density lower --output outputs/effect_h5.mp4
```

### H6 - Nebula (120s)
```bash
python heart_animation.py --effect H6 --resolution large --density lower --output outputs/effect_h6.mp4
```

### H7 - Hologram (90s)
```bash
python heart_animation.py --effect H7 --resolution large --density lower --output outputs/effect_h7.mp4
```

### H8 - Genesis with Music Sync (100s, hardcoded BPM)
```bash
python heart_animation.py --effect H8 --resolution large --density lower --output outputs/effect_h8.mp4
```

## Audio-Synchronized Effects (Require Audio Analysis)

### Step 1: Analyze Audio
```bash
python analyze_audio.py inputs/your_audio.mp3
# Creates: your_audio_features.json
```

### H8sync - Real Audio Sync (100s)
```bash
# After audio analysis:
python heart_animation.py --effect H8sync --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_h8sync.mp4
```

### H8sync3min - Extended Version (210s)
```bash
# After audio analysis:
python heart_animation.py --effect H8sync3min --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_h8sync3min.mp4
```

### H9 - Cuba to New Orleans (~698s)
```bash
# After audio analysis:
python heart_animation.py --effect H9 --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_h9.mp4
```

### H10 - The Mission (~539s)
```bash
# After audio analysis:
python heart_animation.py --effect H10 --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_h10.mp4
```

### I1 - Two Hearts
```bash
# After audio analysis:
python heart_animation.py --effect I1 --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_i1.mp4
```

### I2 - Five Hearts
```bash
# After audio analysis:
python heart_animation.py --effect I2 --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_i2.mp4
```

### I3 - Birthday Celebration
```bash
# After audio analysis:
python heart_animation.py --effect I3 --audio-features your_audio_features.json --resolution large --density lower --output outputs/effect_i3.mp4
```

## Using Build Scripts (Recommended)

### I1 - Two Hearts
```powershell
.\scripts\i1-TwoHearts.ps1 -AudioFile "inputs/your_audio.mp3" -Resolution large -Density lower
```

### I2 - Five Hearts
```powershell
.\scripts\i2-FiveHearts.ps1 -AudioFile "inputs/your_audio.mp3" -Resolution large -Density lower
```

### I3 - Birthday Celebration
```powershell
.\scripts\i3-BirthdayCelebration.ps1 -AudioFile "inputs/Happy Birthday Song.mp3" -Resolution large -Density lower
```

### H9 - Cuba to New Orleans
```powershell
.\scripts\h9-Cuba-NewOrleans.ps1 -Resolution large -Density lower
```

### H10 - The Mission
```powershell
.\scripts\h10-The-Mission.ps1 -Resolution large -Density lower
```

### H8sync3min
```powershell
.\scripts\build_h8sync3min.ps1 -Resolution large -Density lower
```

## Common Options

- `--resolution {small,medium,large,4k}` - Video resolution
- `--density {lower,low,medium,high}` - Point density (lower = faster)
- `--fps {30,60}` - Frame rate
- `--bitrate <kbps>` - Video bitrate (default: 5000)
- `--formulas` - Show parametric formulas
- `--axes` - Show coordinate axes
- `--watermark "TEXT"` - Custom watermark (or `""` to disable)

## Quick Tips

- Use `--density lower` for faster rendering with multi-heart effects (I1, I2, I3)
- Use `--SkipAnalysis` in build scripts if audio features file already exists
- For long effects (H9, H10), expect longer render times
- Multi-heart effects (I1, I2, I3) require more processing time


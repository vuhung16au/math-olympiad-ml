# 3D Heart Animation Generator

A Python script that generates a beautiful 3D rotating heart animation using parametric equations and saves it as an MP4 video.

![Heart Animation](outputs/heart_animation.mp4)

## Overview

This project creates a mesmerizing 3D visualization of a parametric heart shape that rotates 360 degrees around the vertical axis. The heart is rendered using 40,000 points with a stunning magma color gradient against a black background, creating a visually striking animation.

### Key Features

- **Parametric 3D Heart**: Mathematical heart shape defined by parametric equations
- **Smooth Rotation**: 30-second animation with 900 frames at 30 fps
- **Multiple Resolutions**: Choose between small (640x480), medium (1280x720), or large (1920x1080)
- **Beautiful Gradient**: Uses matplotlib's magma colormap for vibrant colors
- **Customizable Parameters**: Easy to tweak rotation speed, colors, view angles, and more

## System Requirements

- **Python**: Version 3.12.10 (or compatible)
- **FFmpeg**: Must be installed and accessible in your system PATH
- **Operating System**: Windows, macOS, or Linux

### Installing FFmpeg

**Windows:**
```powershell
# Using winget
winget install FFmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

Verify installation:
```powershell
ffmpeg -version
```

## Setup Instructions

### 1. Install UV (if not already installed)

UV is a fast Python package installer and environment manager.

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create Virtual Environment

Navigate to the project directory and create a virtual environment:

```powershell
cd MathsHeartShaped3D
uv venv .venv
```

### 3. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```powershell
uv pip install -r requirements.txt
```

## Usage

### Basic Usage (Medium Resolution)

```powershell
python heart_animation.py
```

This will generate a 1280x720 video at `outputs/heart_animation.mp4`.

### Choose Resolution

**Small (640x480) - Fastest:**
```powershell
python heart_animation.py --resolution small
```

**Medium (1280x720) - Default:**
```powershell
python heart_animation.py --resolution medium
```

**Large (1920x1080) - Best Quality:**
```powershell
python heart_animation.py --resolution large
```

### Custom DPI

```powershell
python heart_animation.py --dpi 150
```

### Custom Output Path

```powershell
python heart_animation.py --output my_heart.mp4
```

### Combined Options

```powershell
python heart_animation.py --resolution large --dpi 120 --output outputs/heart_hd.mp4
```

## Expected Runtime

Rendering time depends on your system specifications:

- **Small (640x480)**: ~5-10 minutes
- **Medium (1280x720)**: ~10-20 minutes
- **Large (1920x1080)**: ~20-40 minutes

*Note: Times may vary significantly based on CPU, available RAM, and system load.*

## Output Specifications

- **Duration**: 30 seconds
- **Frame Rate**: 30 fps
- **Total Frames**: 900 frames
- **Rotation**: Full 360-degree rotation around the y-axis
- **Points**: 40,000 data points rendering the heart shape
- **Colormap**: Magma (purple, pink, orange gradient)
- **Background**: Black
- **Format**: MP4 (H.264 codec via FFmpeg)

## Tweaking Parameters

You can modify the script to customize various aspects:

### 1. Rotation Speed

Edit the `total_frames` variable in `create_animation()`:

```python
# Faster rotation (15 seconds)
total_frames = 450  # 15 seconds * 30 fps

# Slower rotation (60 seconds)
total_frames = 1800  # 60 seconds * 30 fps
```

### 2. Color Scheme

Change the colormap in the `create_animation()` function:

```python
# Different colormaps
scatter = ax.scatter(x_original, y_original, z_original, 
                    c=colors, cmap='viridis', s=1, alpha=0.8)  # Green-blue
                    
# Other options: 'plasma', 'inferno', 'twilight', 'cool', 'RdPu'
```

### 3. Initial View Angle

Modify the `setup_figure()` function:

```python
# Top-down view
ax.view_init(elev=90, azim=0)

# Side view
ax.view_init(elev=0, azim=90)

# Custom angle
ax.view_init(elev=30, azim=60)
```

### 4. Marker Size and Transparency

In the `create_animation()` function:

```python
# Larger, more visible points
scatter = ax.scatter(x_original, y_original, z_original, 
                    c=colors, cmap='magma', s=2, alpha=1.0)

# Smaller, more transparent points
scatter = ax.scatter(x_original, y_original, z_original, 
                    c=colors, cmap='magma', s=0.5, alpha=0.6)
```

### 5. Point Density

In the `generate_heart_points()` function:

```python
# More detailed (slower rendering)
x, y, z, colors = generate_heart_points(u_points=300, v_points=300)

# Less detailed (faster rendering)
x, y, z, colors = generate_heart_points(u_points=100, v_points=100)
```

### 6. Video Quality

In the `create_animation()` function:

```python
# Higher quality (larger file size)
writer = FFMpegWriter(fps=30, bitrate=10000)

# Lower quality (smaller file size)
writer = FFMpegWriter(fps=30, bitrate=2000)
```

## Mathematical Background

The 3D heart shape is created using parametric equations with parameters:
- `u` ∈ [0, π]
- `v` ∈ [0, 2π]

**Equations:**
- x = sin(u) · (15sin(v) - 4sin(3v))
- y = 8cos(u)
- z = sin(u) · (15cos(v) - 5cos(2v) - 2cos(3v) - cos(4v))

The rotation is achieved by applying a 3D rotation matrix around the y-axis:
- x' = x·cos(α) + z·sin(α)
- y' = y
- z' = -x·sin(α) + z·cos(α)

Where α is the rotation angle in radians.

## Troubleshooting

### FFmpeg Not Found Error

```
Error: ffmpeg not found in PATH
```

**Solution**: Install FFmpeg and ensure it's in your system PATH. Restart your terminal after installation.

### Memory Error

```
MemoryError: Unable to allocate array
```

**Solution**: Reduce the number of points or resolution:
```powershell
python heart_animation.py --resolution small
```

### Slow Rendering

**Solutions**:
- Use a smaller resolution
- Reduce DPI: `--dpi 80`
- Reduce point count (edit script)
- Close other applications to free up resources

### Module Not Found Error

```
ModuleNotFoundError: No module named 'numpy'
```

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```powershell
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

## Future Improvements and Enhancements

- [ ] Add support for different rotation axes (x-axis, z-axis)
- [ ] Implement multiple camera angles/views in one video
- [ ] Add particle effects or trails
- [ ] Support for GIF output format
- [ ] Real-time preview mode before rendering
- [ ] Add pulsating animation (scale variation)
- [ ] Multiple heart shapes in the same scene
- [ ] Interactive 3D viewer using Plotly or PyVista
- [ ] Stereo 3D / VR output support
- [ ] Custom color gradient designer
- [ ] Audio synchronization (music-reactive animation)
- [ ] Batch rendering with different parameters
- [ ] Progress bar with ETA display
- [ ] GPU acceleration for faster rendering

## Project Structure

```
MathsHeartShaped3D/
├── heart_animation.py      # Main script
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # This file
└── outputs/               # Generated videos
    └── heart_animation.mp4
```

## Dependencies

- **numpy** (>=1.24.0): Numerical computations and array operations
- **matplotlib** (>=3.7.0): 3D visualization and animation
- **FFmpeg**: Video encoding (system dependency)

## License

This project is open source and available for educational and personal use.

## Credits

Created as a demonstration of parametric 3D visualization using Python's scientific computing stack.

---

**Enjoy your beautiful rotating heart animation! ❤️**

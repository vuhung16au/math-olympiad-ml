# 3D Heart Animation Generator

A Python script that generates a beautiful 3D rotating heart animation using parametric equations and saves it as an MP4 video.

![Heart Animation](outputs/heart_animation.mp4)

## Overview

This project creates a mesmerizing 3D visualization of a parametric heart shape with multiple animation effects. The heart can be rendered with various point densities, animated with different rotation and camera effects, and exported at multiple resolutions.

### Key Features

- **Parametric 3D Heart**: Mathematical heart shape defined by parametric equations
- **Multiple Animation Effects**: 4 different animation modes (multi-axis rotation, camera orbit, combined effects, custom)
- **Flexible Point Density**: Choose from ~5K to 40K points for speed vs quality trade-off
- **Multiple Resolutions**: Small (640x480), medium (1280x720), or large (1920x1080)
- **Beautiful Gradient**: Uses matplotlib's magma colormap for vibrant colors
- **Formula Display**: Optionally show parametric equations on the animation
- **Coordinate Axes**: Optional X, Y, Z axis visualization
- **Build Script**: PowerShell script for easy batch rendering
- **30-Second Animation**: 900 frames at 30 fps for smooth playback

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

### Quick Start with Build Script

The easiest way to generate animations is using the `build.ps1` script:

```powershell
# Generate small resolution (640x480) - fastest
.\build.ps1 small

# Generate medium resolution (1280x720) - balanced
.\build.ps1 medium

# Generate large resolution (1920x1080) - best quality
.\build.ps1 large
```

The build script will:
- ✓ Validate Python and FFmpeg installation
- ✓ Check virtual environment setup
- ✓ Display estimated render time
- ✓ Ask for confirmation before rendering
- ✓ Show progress during generation
- ✓ Display final file size and render time

Output files are saved as: `outputs/heart_animation-{size}.mp4`

### Direct Python Script Usage

For more control over animation parameters, use the Python script directly:

**Basic Usage (Default Settings):**
```powershell
python heart_animation.py
```

This generates: medium resolution, low density, effect A (multi-axis rotation)

This generates: medium resolution, low density, effect A (multi-axis rotation)

### Resolution Options

```powershell
# Small (640x480) - fastest rendering
python heart_animation.py --resolution small

# Medium (1280x720) - default
python heart_animation.py --resolution medium

# Large (1920x1080) - best quality
python heart_animation.py --resolution large
```

### Point Density Options

Control the number of points rendering the heart shape:

```powershell
# Lower (~5,000 points) - fastest, good for testing
python heart_animation.py --density lower

# Low (10,000 points) - default, good balance
python heart_animation.py --density low

# Medium (22,500 points) - higher quality
python heart_animation.py --density medium

# High (40,000 points) - best quality, slower
python heart_animation.py --density high
```

**Recommended combinations:**
- Testing: `--resolution small --density lower` (fastest)
- Preview: `--resolution medium --density low` (default)
- Final output: `--resolution large --density high` (best quality)

### Animation Effects

Choose from 4 different animation styles:

**Effect A - Multi-axis Rotation (Default):**
```powershell
python heart_animation.py --effect A
```
- Heart rotates around Y-axis (vertical)
- Adds gentle X-axis wobble for depth
- Creates dynamic 3D perception

**Effect B - Dynamic Camera Orbit:**
```powershell
python heart_animation.py --effect B
```
- Heart remains stationary
- Camera circles around the heart (360°)
- Elevation changes create dramatic angles
- Best for showcasing the heart shape

**Effect C - Combined Effects:**
```powershell
python heart_animation.py --effect C
```
- Heart rotates around Y-axis (360°)
- Camera orbits halfway around (180°)
- Zoom in during first half, zoom out during second half
- Most cinematic and complex effect

**Effect D - Custom Animation:**
```powershell
python heart_animation.py --effect D
```
- Heart rotates around Y-axis
- Camera elevation sweeps from low to high
- Subtle zoom pulse synchronized with rotation
- Unique vertical perspective changes

### Display Options

```powershell
# Hide coordinate axes
python heart_animation.py --no-axes

# Hide parametric formulas
python heart_animation.py --no-formulas

# Hide both
python heart_animation.py --no-axes --no-formulas
```

### Advanced Options

**Custom DPI (rendering quality):**rendering quality):**
```powershell
python heart_animation.py --dpi 150
```

**Custom Output Path:**
```powershell
python heart_animation.py --output my_heart.mp4
```

### Combined Examples

```powershell
# Quick test render
python heart_animation.py --resolution small --density lower --effect A

# High-quality cinematic render
python heart_animation.py --resolution large --density high --effect C

# Camera orbit with medium quality
python heart_animation.py --resolution medium --density medium --effect B

# Clean render without annotations
python heart_animation.py --resolution large --effect D --no-axes --no-formulas

# Custom quality settings
python heart_animation.py --resolution medium --dpi 120 --density medium --effect C --output outputs/heart_hd.mp4
```

## Expected Runtime

Rendering time depends on resolution, density, and your system specifications:

| Resolution | Density | Approximate Time |
|------------|---------|------------------|
| Small      | Lower   | 2-5 minutes      |
| Small      | Low     | 3-7 minutes      |
| Medium     | Low     | 8-15 minutes     |
| Medium     | Medium  | 15-25 minutes    |
| Large      | Medium  | 25-40 minutes    |
| Large      | High    | 40-70 minutes    |

**Notes:**
- Effect types don't significantly impact render time
- Times vary based on CPU, RAM, and system load
- The build script shows estimated times before rendering
- Progress updates appear every second during generation

## Output Specifications

- **Duration**: 30 seconds
- **Frame Rate**: 30 fps
- **Total Frames**: 900 frames
- **Animation**: Full 360-degree rotation (varies by effect mode)
- **Point Density**: ~5,000 to 40,000 data points
- **Colormap**: Magma (purple, pink, orange gradient)
- **Background**: Black
- **Format**: MP4 (H.264 codec via FFmpeg)
- **Effects**: 4 different animation styles
- **Display Options**: Optional formulas and coordinate axes

## Tweaking Parameters

You can modify the script to customize various aspects. For most use cases, the command-line options provide sufficient control. For advanced customization, edit the script directly:

### 1. Animation Duration

Edit the `total_frames` variable in `create_animation()`:

```python
# Faster animation (15 seconds)
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

### 3. Initial View Angle (for non-animated camera modes)

Modify the `setup_figure()` function:

```python
# Top-down view
ax.view_init(elev=90, azim=0)

# Side view
ax.view_init(elev=0, azim=90)

# Custom angle
ax.view_init(elev=30, azim=60)
```

Note: Effects B, C, and D override the initial view angle with dynamic camera movements.

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

### 5. Custom Point Density (advanced)

Use command-line options instead: `--density lower|low|medium|high`

For custom values, edit the `generate_heart_points()` function:

```python
# Ultra detailed (very slow rendering)
density_multipliers = {'ultra': 1.5}  # 300x300 = 90,000 points
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

**Solution**: Reduce the point density or resolution:
```powershell
# Try lower density
python heart_animation.py --density lower

# Or smaller resolution
python heart_animation.py --resolution small --density low
```

### Slow Rendering

**Solutions**:
- Use lower density: `--density lower` or `--density low`
- Use smaller resolution: `--resolution small`
- Reduce DPI: `--dpi 80`
- Use simpler effects: `--effect A` (default)
- Close other applications to free up resources

**Quick test render:**
```powershell
python heart_animation.py --resolution small --density lower --effect A
```

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

- [x] Multiple animation effects (A, B, C, D)
- [x] Flexible point density options
- [x] Formula and axes display
- [x] PowerShell build script
- [ ] Support for different primary rotation axes
- [ ] Multiple hearts in one scene
- [ ] Particle effects or trails
- [ ] GIF output format
- [ ] Real-time preview mode
- [ ] Pulsating animation (scale variation)
- [ ] Interactive 3D viewer using Plotly
- [ ] Stereo 3D / VR output
- [ ] Custom color gradient designer
- [ ] Audio synchronization (music-reactive)
- [ ] Batch rendering different configurations
- [ ] Enhanced progress bar with ETA
- [ ] GPU acceleration for faster rendering

## Project Structure

```
MathsHeartShaped3D/
├── heart_animation.py         # Main Python script with animation logic
├── build.ps1                  # PowerShell build script for easy rendering
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── README.md                 # This documentation
└── outputs/                  # Generated video files
    ├── heart_animation-small.mp4
    ├── heart_animation-medium.mp4
    └── heart_animation-large.mp4
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

# Drone Show Simulation

A Python-based simulation system for choreographing 1000 drones in spectacular aerial formations including hearts, stars, and text displays with physics-based movement and collision avoidance.

![Drone Show](outputs/drone_show.mp4)

## Overview

This project simulates a complete drone show with realistic physics, collision avoidance, and cinematic camera work. The system generates both video animations and exportable flight paths for real-world drone operations.

### Key Features

- **1000 Drones**: Full swarm simulation with individual physics
- **2D Formations**: Industry-standard flat formations in Y-Z plane for optimal visibility
- **Multiple Shapes**: Heart (900 drones), 5-pointed star (850 drones), text displays (700-900 drones)
- **60m × 60m Scale**: Large formations (60m × 60m) to accommodate 800-900 drones with proper spacing
- **Collision Avoidance**: Path priority algorithm ensures minimum 2m separation
- **Physics Simulation**: Realistic acceleration (2 m/s²), max speed (4 m/s), and position drift
- **Fixed Audience View**: Camera positioned like real drone show audience (150m in front)
- **Path Export**: JSON and CSV formats for real-world drone operations
- **Flexible Timing**: Testing mode (16s) and production mode (120s)
- **4K Output**: High-quality video rendering at 3840×2160

## Design Philosophy: 2D vs 3D

This simulation uses **2D formations** (flat shapes in the Y-Z plane) rather than 3D, matching real-world drone show best practices:

### Why 2D?

1. **Optimal Visibility**: Flat formations are clearly visible from audience perspective
2. **Industry Standard**: Professional drone shows (Intel, Pixar, etc.) use 2D formations
3. **Simplified Logistics**: Easier collision avoidance and flight path planning
4. **Better Recognition**: Shapes and text are immediately recognizable when viewed head-on
5. **Scalability**: 60m × 60m formations accommodate 900 drones with 2m spacing

### Camera Configuration

- **Position**: Fixed at (150m, 0, 15m) - simulates audience view 150m in front
- **Target**: (0, 0, 15m) - center of formation area at 15m altitude
- **Field of View**: 60° covers 173m width - plenty of room for 60m formations
- **Orientation**: Direct front view of Y-Z plane formations

## System Requirements

- **Python**: 3.9 or higher
- **FFmpeg**: Required for video rendering
- **UV**: Fast Python package manager
- **Operating System**: macOS, Linux, or Windows

### Installing Dependencies

**UV (Package Manager):**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**FFmpeg:**
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Windows
winget install FFmpeg
```

Verify installation:
```bash
ffmpeg -version
```

## Quick Start

### 1. Clone or Download

```bash
cd DroneShow
```

### 2. Setup Environment

**Option A: Using Makefile (Recommended)**
```bash
make setup
```

**Option B: Using Shell Script**
```bash
./scripts/setup.sh
```

**Option C: Manual Setup**
```bash
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Run Drone Show

**Quick test (16 seconds):**
```bash
make drone-show
# Or: ./scripts/run-testing.sh
# Or: python drone_show.py --mode testing
```

**Full production (120 seconds):**
```bash
make drone-show-production
# Or: ./scripts/run-production.sh
# Or: python drone_show.py --mode production
```

## Scene Timeline

The show consists of 8 scenes:

| Scene | Description | Active Drones | Color |
|-------|-------------|---------------|-------|
| 1. Blackout | All drones parked, lights off | 0 | - |
| 2. Heart | 3D parametric heart | 700 | Red |
| 3. Star | 5-pointed star | 500 | Gold |
| 4. VIETNAM | Text with gradient | 350 | Yellow → Red |
| 5. AUSTRALIA | Text with gradient | 400 | Green → Gold |
| 6. I ❤ VIETNAM | Combined text + emoji | 480 | White + Gradient |
| 7. I ❤ AUSTRALIA | Combined text + emoji | 530 | White + Gradient |
| 8. Blackout | Return to parking | 0 | - |

**Timing:**
- **Testing Mode**: 2 seconds per scene (16 seconds total)
- **Production Mode**: 15 seconds per scene (120 seconds total)
- **Transitions**: 1-second cross-fade between scenes

## Usage

### Command-Line Options

```bash
python drone_show.py [OPTIONS]
```

**Options:**
- `--mode, -m`: `testing` (16s) or `production` (120s) - default: `testing`
- `--fps`: Frames per second - default: `30`
- `--output, -o`: Output video path - default: `outputs/drone_show.mp4`
- `--export-paths`: Export flight paths to JSON/CSV
- `--info`: Show scene information and exit (no rendering)

### Examples

**Quick test render:**
```bash
python drone_show.py
```

**Production render with path export:**
```bash
python drone_show.py --mode production --export-paths
```

**Custom output path:**
```bash
python drone_show.py --mode testing --output my_show.mp4
```

**Show scene information:**
```bash
python drone_show.py --info
```

## Makefile Commands

```bash
make venv              # Create virtual environment
make setup             # Setup venv and install dependencies
make drone-show        # Run testing mode (16s)
make drone-show-production  # Run production mode (120s)
make export-paths      # Export flight paths
make test              # Run tests (when implemented)
make clean-drone       # Clean drone show outputs
make clean-venv        # Remove virtual environment
make clean-all         # Clean everything
```

## Shell Scripts

Located in `scripts/` directory:

- `setup.sh` - Setup environment and dependencies
- `run-testing.sh` - Run testing mode
- `run-production.sh` - Run production mode
- `export-paths.sh` - Export flight paths
- `clean.sh` - Clean outputs and cache

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

## Path Export for Real-World Operations

The system can export complete flight paths for actual drone operations:

```bash
python drone_show.py --export-paths
```

**Generates:**
- `outputs/drone_show_paths.json` - Complete structured data
- `outputs/drone_show_paths.csv` - Spreadsheet-compatible format
- `outputs/drone_show_paths_validation.txt` - Safety validation report

**Export format includes:**
- Timestamp (0.1s intervals)
- Position (x, y, z) in meters
- Color (RGB 0-255)
- Light state (on/off)
- Metadata (duration, drone count, validation)

## Performance Space

- **Volume**: 100m (W) × 100m (D) × 30m (H)
- **Origin**: Center at ground level (0, 0, 0)
- **Formation center**: (0, 0, 15) - 15m altitude
- **Parking area**: Ground level in 90m × 90m grid

## Drone Physics

- **Max speed**: 4 m/s
- **Acceleration**: 2 m/s² (reaches max speed in 2 seconds)
- **Deceleration**: 2 m/s²
- **Minimum separation**: 2 meters (collision avoidance)
- **Position accuracy**: ±0.1m random drift
- **Movement**: Smooth ease-in-ease-out curves

## Camera System

- **Target**: (0, 0, 10) - center of performance space
- **Orbit radius**: 200 meters
- **Orbit period**: 360° in 20 seconds
- **Height**: 100-200m above ground
- **Field of view**: 60 degrees
- **Behavior**: Continuous orbital movement

## Video Output

- **Resolution**: 4K (3840 × 2160)
- **Frame rate**: 30 fps
- **Bitrate**: 5000 kbps
- **Codec**: H.264
- **Format**: MP4
- **Background**: Black

## Project Structure

```
DroneShow/
├── drone_show.py              # Main entry point
├── config/
│   └── drone_config.py        # Configuration constants
├── core/
│   ├── drone_system.py        # Drone physics and state management
│   ├── shape_generators.py    # Formation generators
│   ├── path_planner.py        # Path planning with collision avoidance
│   ├── path_exporter.py       # Export paths for real-world operations
│   ├── scene_controller.py    # Scene timeline management
│   ├── camera_controller.py   # Orbiting camera system
│   ├── heart_generator.py     # Parametric heart equations (reused)
│   └── figure_setup.py        # Matplotlib setup utilities (reused)
├── scripts/
│   ├── setup.sh               # Environment setup
│   ├── run-testing.sh         # Run testing mode
│   ├── run-production.sh      # Run production mode
│   ├── export-paths.sh        # Export flight paths
│   └── clean.sh               # Clean outputs
├── tests/                     # Test suite (to be implemented)
├── outputs/                   # Generated videos and paths
├── Makefile                   # Build automation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Dependencies

- **numpy** (>=1.24.0) - Numerical computations
- **matplotlib** (>=3.7.0) - 3D visualization and animation
- **scipy** (>=1.10.0) - Optimal assignment algorithms
- **pytest** (>=7.0.0) - Testing framework
- **tqdm** (>=4.65.0) - Progress bars
- **FFmpeg** - Video encoding (system dependency)

## Configuration

All parameters can be customized in `config/drone_config.py`:

- Performance space dimensions
- Drone physics constants
- Camera settings
- Scene timing
- Color schemes
- Formation parameters

## Troubleshooting

### FFmpeg Not Found

```
Error: FFmpeg not found
```

**Solution**: Install FFmpeg and ensure it's in your PATH.

### Virtual Environment Issues

```
Error: No module named 'numpy'
```

**Solution**: Activate virtual environment and reinstall dependencies:
```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Slow Rendering

**Tips**:
- Use testing mode for quick iteration
- Close other applications
- Ensure sufficient RAM (8GB+ recommended)

### Memory Errors

**Solution**: The simulation is optimized for 1000 drones. If issues persist:
- Close other applications
- Use lower resolution (edit VIDEO_RESOLUTION in config)

## Technical Implementation

### Collision Avoidance

The system uses a **Path Priority Algorithm**:
1. Pre-calculate all drone paths before animation
2. Detect conflicts (drones within 2m at any time)
3. Resolve by delaying lower-priority drones
4. Priority based on drone ID (lower ID = higher priority)

### Path Planning

Uses Hungarian algorithm (scipy) for optimal drone-to-target assignment:
- Minimizes total travel distance
- Ensures smooth transitions between formations
- Applies ease-in-ease-out curves for natural motion

### Scene Transitions

Smooth 1-second cross-fade between scenes:
- Interpolate positions with easing
- Blend colors linearly
- Maintain collision avoidance during transitions

## Future Enhancements

- [ ] Music synchronization with beat detection
- [ ] Wind effects and environmental factors
- [ ] Battery level simulation
- [ ] More complex formations
- [ ] Multiple camera angles
- [ ] Interactive real-time preview
- [ ] Export to actual drone show formats (.csv for commercial systems)
- [ ] Comprehensive test suite
- [ ] Performance optimizations

## Credits

Built on top of the 3D Heart Animation project, extending it into a full drone show simulation system.

---

**Ready for takeoff! 🚁**

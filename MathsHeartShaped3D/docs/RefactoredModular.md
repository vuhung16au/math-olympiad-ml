# Refactored Modular Architecture

## Overview

The `heart_animation.py` script has been successfully refactored from a monolithic ~1810-line file into a clean, modular architecture with ~360 lines in the main file. The refactoring improves maintainability, extensibility, and code organization while maintaining 100% backward compatibility with the existing CLI interface.

## New Directory Structure

```
MathsHeartShaped3D/
├── core/                    # Core functionality modules
│   ├── __init__.py
│   ├── heart_generator.py   # Heart point generation
│   ├── figure_setup.py      # Matplotlib figure setup
│   └── audio_sync.py        # Audio synchronization helpers
├── effects/                  # Animation effects
│   ├── __init__.py          # BaseEffect class and registry
│   ├── effect_a.py          # Effect A: Multi-axis rotation
│   ├── effect_b.py          # Effect B: Dynamic camera orbit
│   ├── effect_c.py          # Effect C: Combined
│   ├── effect_d.py          # Effect D: Custom
│   ├── effect_e.py          # Effect E: Heartbeat Pulse
│   ├── effect_f.py          # Effect F: Spiral Ascent
│   ├── effect_g.py          # Effect G: Figure-8 Dance
│   ├── effect_g1.py         # Effect G1: Heart Journey
│   ├── effect_g2.py         # Effect G2: Epic Heart Story
│   ├── effect_h1.py         # Effect H1: Heart Genesis
│   ├── effect_h2.py         # Effect H2: Time Reversal
│   ├── effect_h3.py         # Effect H3: Fractal Heart
│   ├── effect_h4.py         # Effect H4: Dual Hearts
│   ├── effect_h5.py         # Effect H5: Kaleidoscope Heart
│   ├── effect_h6.py         # Effect H6: Heart Nebula
│   ├── effect_h7.py         # Effect H7: Hologram Heart
│   ├── effect_h8.py         # Effect H8: Heart Genesis with Music Sync
│   └── effect_h8sync.py    # Effect H8sync: Real Audio Sync
├── config/                   # Configuration
│   ├── __init__.py
│   └── heart_config.py      # Configurable heart formula parameters
└── heart_animation.py       # Main script (refactored)
```

## Core Modules

### `core/heart_generator.py`

Handles the generation of 3D heart coordinates using configurable parametric equations.

**Key Features:**
- Configurable point density (lower, low, medium, high)
- Uses formula from `config/heart_config.py`
- Returns x, y, z coordinates and color values

**Usage:**
```python
from core.heart_generator import generate_heart_points

x, y, z, colors = generate_heart_points(density='high')
```

### `core/figure_setup.py`

Sets up the matplotlib figure and 3D axes with configurable options.

**Key Features:**
- Resolution presets (small, medium, large, 4k)
- Optional coordinate axes
- Optional formula display
- Watermark support

**Usage:**
```python
from core.figure_setup import setup_figure

fig, ax = setup_figure(resolution='medium', dpi=100, 
                       show_axes=False, show_formulas=True, 
                       watermark='VUHUNG')
```

### `core/audio_sync.py`

Provides helper functions for audio synchronization in effects.

**Functions:**
- `get_beat_intensity()` - Get beat intensity at current time
- `get_onset_intensity()` - Get onset intensity at current time
- `get_loudness_at_time()` - Get normalized loudness (0-1)
- `get_bass_at_time()` - Get bass strength (0-1)
- `get_tempo_at_time()` - Get tempo in BPM

**Usage:**
```python
from core.audio_sync import get_beat_intensity

beat_intensity = get_beat_intensity(current_second, beat_times, window=0.1)
```

## Configuration

### `config/heart_config.py`

Stores configurable parameters for the heart formula.

**Current Formula (Original Trio Formula):**
- `x = sin(u) · (15sin(v) - 4sin(3v))`
- `y = 8cos(u)` (flipped vertically)
- `z = sin(u) · (15cos(v) - 5cos(2v) - 2cos(3v) - cos(v))`

**Configuration Structure:**
```python
HEART_FORMULA = {
    'x_coeffs': [15, -4],      # [sin(v) coefficient, sin(3v) coefficient]
    'y_coeff': 8,              # cos(u) coefficient
    'z_coeffs': [15, -5, -2, -1],  # [cos(v), cos(2v), cos(3v), cos(v)] coefficients
    'y_flip': True             # If True, negate y to flip vertically
}
```

**To customize the formula:**
1. Edit `config/heart_config.py`
2. Modify `HEART_FORMULA` dictionary
3. Update `FORMULA_DISPLAY` for LaTeX display strings

## Effects System

### BaseEffect Class

All effects inherit from `BaseEffect` in `effects/__init__.py`.

**Required Methods:**
- `get_total_frames()` - Return total number of frames for the effect
- `update(frame)` - Update animation for given frame, return `(scatter,)` tuple

**Initialization Parameters:**
- `total_frames` - Total frames (set after `get_total_frames()`)
- `fps` - Frames per second
- `x_original`, `y_original`, `z_original` - Original heart coordinates
- `scatter` - Matplotlib scatter plot object
- `ax` - Matplotlib 3D axes object
- `audio_features` - Optional dict with audio features for sync

**Helper Methods:**
- `get_normalized_time(frame)` - Get normalized time (0-1)
- `get_current_second(frame)` - Get current time in seconds

### Effect Registry

Effects are automatically registered when their modules are imported.

**Registry Functions:**
- `register_effect(name, effect_class)` - Register an effect
- `get_effect_class(name)` - Get effect class by name
- `get_all_effect_names()` - Get list of all registered effect names

**Example Effect Structure:**
```python
from effects import BaseEffect, register_effect
import numpy as np

class EffectA(BaseEffect):
    """Multi-axis rotation with gentle X-axis wobble."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        t = self.get_normalized_time(frame)
        # ... effect logic ...
        return self.scatter,

# Register the effect
register_effect('A', EffectA)
```

## All 18 Effects

### Basic Effects (A-G)
- **A**: Multi-axis rotation (Y-axis + X-axis wobble) - 30s
- **B**: Dynamic camera orbit (heart stays stationary) - 30s
- **C**: Combined (rotating heart + orbiting camera + zoom) - 30s
- **D**: Custom (Y rotation + elevation sweep + zoom pulse) - 30s
- **E**: Heartbeat Pulse (rotation + rhythmic scaling) - 30s
- **F**: Spiral Ascent (rotation + spiral camera + zoom out) - 30s
- **G**: Figure-8 Dance (rotation + figure-8 camera path) - 30s

### Epic Effects (G1-G2)
- **G1**: Heart Journey (camera zooms through heart, then orbits back) - 90s
- **G2**: Epic Heart Story (multi-phase cinematic sequence) - 137s

### H Series Effects (H1-H8sync)
- **H1**: Heart Genesis (creation story) - 100s
- **H2**: Time Reversal (forward then backward) - 90s
- **H3**: Fractal Heart (recursive hearts) - 90s
- **H4**: Dual Hearts (two hearts dancing) - 120s
- **H5**: Kaleidoscope Heart (mirrored reflections) - 60s
- **H6**: Heart Nebula (cosmic space journey) - 120s
- **H7**: Hologram Heart (wireframe tech aesthetic) - 90s
- **H8**: Heart Genesis with Music Sync (BPM-synchronized beats) - 100s
- **H8sync**: Heart Genesis with Real Audio Sync (librosa-detected features) - 100s

## Main Script Refactoring

### Before Refactoring
- ~1810 lines in single file
- All effects implemented as if/elif chains
- Hard to maintain and extend
- Difficult to test individual effects

### After Refactoring
- ~360 lines in main file
- Effects organized in separate modules
- Easy to add new effects
- Testable components
- Clear separation of concerns

### Key Changes in `heart_animation.py`

1. **Imports from new modules:**
```python
from core.heart_generator import generate_heart_points
from core.figure_setup import setup_figure
from effects import get_effect_class
```

2. **Effect instantiation:**
```python
EffectClass = get_effect_class(effect)
if EffectClass is None:
    # Fallback to simple rotation
else:
    effect_instance = EffectClass(...)
    total_frames = effect_instance.get_total_frames()
    # Create update function that delegates to effect
```

3. **Special handling for H4:**
```python
if effect == 'H4':
    # Generate second heart
    x_heart2, y_heart2, z_heart2, colors2 = generate_heart_points(density=density)
    # Pass to effect instance
    effect_instance = EffectClass(..., x_heart2=x_heart2, ...)
```

## Backward Compatibility

**100% backward compatible** - All existing CLI commands work exactly as before:

```bash
# All these commands work identically
python heart_animation.py
python heart_animation.py --effect A
python heart_animation.py --effect H8sync --audio-features features.json
python heart_animation.py --resolution 4k --effect G2
```

No changes required to:
- Command-line arguments
- Output format
- Effect names
- Configuration options

## Adding New Effects

To add a new effect:

1. **Create effect file** `effects/effect_new.py`:
```python
from effects import BaseEffect, register_effect
import numpy as np

class EffectNew(BaseEffect):
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        t = self.get_normalized_time(frame)
        # Your effect logic here
        return self.scatter,

register_effect('New', EffectNew)
```

2. **Import in `effects/__init__.py`**:
```python
from . import effect_new
```

3. **Add to CLI choices** in `heart_animation.py`:
```python
parser.add_argument('--effect', choices=[..., 'New'], ...)
```

4. **Add to effect_names dictionary**:
```python
effect_names = {
    ...
    'New': 'Description of new effect',
}
```

## Benefits of Refactoring

1. **Maintainability**: Each effect is isolated in its own file
2. **Extensibility**: Easy to add new effects without touching existing code
3. **Testability**: Individual effects can be tested independently
4. **Readability**: Smaller, focused files are easier to understand
5. **Reusability**: Core modules can be reused in other projects
6. **Configuration**: Heart formula is now configurable without code changes

## File Size Comparison

| Component | Before | After |
|-----------|--------|-------|
| Main script | ~1810 lines | ~360 lines |
| Effects | N/A (inline) | 18 files, ~50-200 lines each |
| Core modules | N/A (inline) | 3 files, ~50-100 lines each |
| Config | N/A (hardcoded) | 1 file, ~50 lines |

## Testing

All effects are registered and accessible:

```python
from effects import get_all_effect_names, get_effect_class

# Get all registered effects
effects = get_all_effect_names()
# ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'G1', 'G2', 
#  'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H8sync']

# Get specific effect class
EffectA = get_effect_class('A')
```

## Future Enhancements

The modular architecture enables:

1. **Effect plugins**: Load effects from external files
2. **Effect composition**: Combine multiple effects
3. **Effect parameters**: Configurable effect parameters
4. **Effect presets**: Save/load effect configurations
5. **Effect preview**: Quick preview of effects before full render
6. **Parallel rendering**: Render multiple effects simultaneously

## Conclusion

The refactoring successfully transforms a monolithic script into a clean, modular architecture while maintaining full backward compatibility. The new structure makes the codebase more maintainable, extensible, and easier to work with, setting a solid foundation for future enhancements.


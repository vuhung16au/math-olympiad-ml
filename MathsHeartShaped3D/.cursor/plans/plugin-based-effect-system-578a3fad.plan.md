<!-- 578a3fad-a4ec-4d97-a9f1-c9f41096cda1 767ca4d2-1889-4a7b-81c5-db20dadd1447 -->
# Plugin-Based Effect System

## Goal

Make adding new effects as simple as creating a new file in `effects/` folder - no modifications to `heart_animation.py` required. Refactor all existing effects to use the new plugin system for consistency.

## Architecture Overview

### 1. Effect Metadata System (`core/effect_metadata.py`)

- Create `@effect_metadata()` decorator that accepts:
  - `num_hearts`: Number of additional hearts needed (default: 0)
  - `requires_audio`: Whether audio features are required (default: False)
  - `default_duration`: Default duration in seconds if no audio (default: 30)
  - `description`: Human-readable description
  - `colormaps`: List of colormaps for each heart (optional)
- Metadata stored as class attribute `_effect_metadata`
- Effects can access metadata via `self.metadata` property

### 2. Effect Resource Provider (`core/effect_resources.py`)

- Create `EffectResourceProvider` class that:
  - Generates hearts on demand: `create_heart(density, colormap)`
  - Creates scatter plots: `create_scatter(x, y, z, colors, colormap, alpha)`
  - Provides heart data lists for multi-heart effects
  - Manages all resource creation centrally
- Effects request resources via provider instead of receiving them as parameters

### 3. Auto-Discovery System (`effects/__init__.py`)

- Add `discover_effects()` function that:
  - Scans `effects/` folder for `effect_*.py` files
  - Dynamically imports them
  - Extracts metadata from decorators
  - Registers effects automatically
- Remove manual imports (no longer needed)
- Update `get_effect_class()` to use discovered effects

### 4. Generic Effect Factory (`core/effect_factory.py`)

- Create `EffectFactory` class that:
  - Takes effect name and metadata
  - Determines required resources from metadata
  - Generates hearts and scatter plots as needed
  - Instantiates effect with appropriate kwargs
  - Uses metadata to determine what to pass to effect constructor

### 5. Refactor `heart_animation.py`

- Remove hardcoded effect-specific logic (lines 107-262)
- Replace with generic factory pattern:
  ```python
  factory = EffectFactory(ax, density, audio_features)
  effect_instance = factory.create_effect(effect, x_original, y_original, z_original, scatter)
  ```

- Update argparse to auto-discover effect choices dynamically
- Remove manual effect name lists

### 6. Update BaseEffect Class (`effects/__init__.py`)

- Add optional `metadata` property
- Add `prepare_resources(provider)` method for effects that need custom resource setup
- Update `__init__` to accept optional `resource_provider` parameter
- Effects can override `prepare_resources()` for custom initialization

### 7. Refactor All Existing Effects

Convert all 24 existing effects to use the new plugin system:

- **Simple effects (A-G)**: Add `@effect_metadata()`, use standard BaseEffect
- **Epic effects (G1, G2)**: Add metadata with `default_duration`
- **H series (H1-H10)**: Add metadata, convert audio-sync ones with `requires_audio=True`
- **Multi-heart effects (H4, I1, I2, I3)**: Add metadata with `num_hearts`, use `prepare_resources()`
- Remove all custom `__init__` parameters
- Update all effects to use resource provider

### 8. Documentation

- Create `docs/creating_effects.md` with:
  - Template for new effects
  - Metadata options explained
  - Examples (simple, multi-heart, audio-sync)
  - Complete reference guide

## Implementation Steps

1. Create `core/effect_metadata.py` with decorator system
2. Create `core/effect_resources.py` with resource provider
3. Create `core/effect_factory.py` with generic factory
4. Update `effects/__init__.py` with auto-discovery
5. Update `BaseEffect` class with metadata support
6. Refactor `heart_animation.py` to use factory (remove all hardcoded logic)
7. Convert all 24 existing effects to new system:

   - Phase 1: Simple effects (A, B, C, D, E, F, G) - 7 effects
   - Phase 2: Epic effects (G1, G2) - 2 effects
   - Phase 3: H series (H1-H7, H8, H8sync, H8sync3min, H9, H10) - 11 effects
   - Phase 4: I series (I1, I2, I3) - 3 effects
   - Phase 5: H4 (dual hearts) - 1 effect

8. Update argparse to auto-discover effect choices
9. Update documentation
10. Test all effects to ensure they work correctly

## Benefits

- Add new effect: Just create `effects/effect_i4.py` with `@effect_metadata()` - done!
- No changes to `heart_animation.py` needed
- Human-readable: Metadata clearly shows what effect needs
- Auto-discovery: Effects automatically available
- Consistent: All effects use the same plugin system
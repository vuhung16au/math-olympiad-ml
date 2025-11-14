# Animation Effects Guide

This document describes all available animation effects for the 3D Heart Animation project. Each effect creates a unique visual experience with different camera movements, rotations, and zoom behaviors.

## Table of Contents

- [Effect A: Multi-Axis Rotation](#effect-a-multi-axis-rotation)
- [Effect B: Dynamic Camera Orbit](#effect-b-dynamic-camera-orbit)
- [Effect C: Combined](#effect-c-combined)
- [Effect D: Custom](#effect-d-custom)
- [Effect E: Heartbeat Pulse](#effect-e-heartbeat-pulse)
- [Effect F: Spiral Ascent](#effect-f-spiral-ascent)
- [Effect G: Figure-8 Dance](#effect-g-figure-8-dance)
- [Effect G1: Heart Journey](#effect-g1-heart-journey)
- [Effect G2: Epic Heart Story](#effect-g2-epic-heart-story)
- [Comparison Table](#comparison-table)
- [Usage Examples](#usage-examples)

---

## Effect A: Multi-Axis Rotation

**Duration:** 30 seconds  
**Complexity:** Simple  
**Best For:** Basic demonstrations, quick renders

### Description
The classic effect featuring a smooth rotation of the heart around the Y-axis (vertical) with a gentle wobble on the X-axis. This creates a natural, rhythmic motion that showcases the heart's 3D structure.

### Technical Details
- **Primary Rotation:** 360° around Y-axis (vertical)
- **Secondary Motion:** ±15° wobble on X-axis
- **Wobble Frequency:** 2 cycles per rotation
- **Camera:** Fixed position (elevation: 20°, azimuth: 45°)
- **Zoom:** Constant (factor: 20)

### Visual Characteristics
- Smooth, predictable motion
- Heart maintains upright orientation
- Gentle rocking motion adds depth
- Full 360° view of the heart

### Command
```powershell
python heart_animation.py --effect A --resolution medium --density low
```

---

## Effect B: Dynamic Camera Orbit

**Duration:** 30 seconds  
**Complexity:** Simple  
**Best For:** Observing heart from multiple angles

### Description
The heart remains stationary while the camera orbits around it, providing a complete 360° view. The camera elevation oscillates smoothly to create a dynamic viewing experience.

### Technical Details
- **Heart Rotation:** None (stationary)
- **Camera Orbit:** 360° horizontal rotation
- **Elevation Range:** 20° to 40° (oscillates)
- **Elevation Frequency:** 1 cycle per orbit
- **Starting Azimuth:** 45°
- **Zoom:** Constant (factor: 20)

### Visual Characteristics
- Heart remains fixed in space
- Camera circles around heart
- Elevation changes create dramatic angles
- Ideal for studying heart shape

### Command
```powershell
python heart_animation.py --effect B --resolution medium --density low
```

---

## Effect C: Combined

**Duration:** 30 seconds  
**Complexity:** Moderate  
**Best For:** Dynamic presentations, showcase videos

### Description
A combination effect where the heart rotates on its axis while the camera simultaneously orbits around it and zooms in and out. Creates a rich, engaging visual experience.

### Technical Details
- **Heart Rotation:** 360° around Y-axis
- **Camera Orbit:** 180° horizontal rotation
- **Elevation Range:** 20° to 35° (oscillates)
- **Zoom Pattern:** 
  - First 15s: Zoom in (20 → 15)
  - Last 15s: Zoom out (15 → 20)
- **Coordination:** All movements synchronized

### Visual Characteristics
- Layered motion (heart + camera + zoom)
- Zoom creates intimacy then reveals context
- Slower camera orbit (180°) complements rotation
- Most visually complex short effect

### Command
```powershell
python heart_animation.py --effect C --resolution medium --density medium
```

---

## Effect D: Custom

**Duration:** 30 seconds  
**Complexity:** Moderate  
**Best For:** Professional presentations, artistic videos

### Description
A carefully choreographed effect featuring Y-axis rotation combined with a dramatic elevation sweep and subtle zoom pulsing. The camera moves from bottom to top view and back.

### Technical Details
- **Heart Rotation:** 360° around Y-axis
- **Camera Azimuth:** Fixed at 45°
- **Elevation Sweep:** 20° → 60° → 20° (sinusoidal)
- **Zoom Pulse:** 
  - Base: 20
  - Amplitude: ±3
  - Frequency: 4 pulses per rotation
- **Breathing Effect:** Zoom pulse creates "breathing" feel

### Visual Characteristics
- Smooth elevation sweep reveals top and bottom
- Rhythmic zoom pulse adds energy
- Heart rotation provides base motion
- Elegant, professional look

### Command
```powershell
python heart_animation.py --effect D --resolution medium --density medium
```

---

## Effect E: Heartbeat Pulse

**Duration:** 30 seconds  
**Complexity:** Moderate  
**Best For:** Medical/health content, Valentine's Day videos

### Description
The heart rotates while pulsating in size, mimicking a real heartbeat with a distinctive "lub-dub" rhythm. Creates an organic, living appearance.

### Technical Details
- **Heart Rotation:** 360° around Y-axis
- **Heartbeat Pattern:** Double pulse (lub-dub)
- **Scale Range:** 1.0 to 1.15 (15% expansion)
- **Pulse Frequency:** 2 beats per rotation
- **Secondary Pulse:** Offset by 60° (π/3)
- **Camera Wobble:** ±5° elevation synchronized with beat
- **Zoom:** Constant (factor: 20)

### Visual Characteristics
- Realistic heartbeat rhythm
- Heart expands and contracts
- Camera wobbles subtly with beat
- Creates sense of life and motion
- "Lub-dub" pattern clearly visible

### Command
```powershell
python heart_animation.py --effect E --resolution medium --density low
```

---

## Effect F: Spiral Ascent

**Duration:** 30 seconds  
**Complexity:** High  
**Best For:** Dramatic reveals, artistic presentations

### Description
A cinematic effect where the camera spirals upward while orbiting the rotating heart, simultaneously zooming out. Creates a grand, sweeping motion.

### Technical Details
- **Heart Rotation:** 360° around Y-axis
- **Camera Orbit:** 720° (2 complete rotations)
- **Elevation Rise:** -10° to 60° (70° range)
- **Zoom Out:** 20 → 35 (linear)
- **Spiral Motion:** Combines orbit + elevation + zoom
- **Velocity:** Constant upward motion

### Visual Characteristics
- Dramatic ascending camera movement
- Double spiral creates dynamic motion
- Gradually reveals heart from different heights
- Zoom out adds scale and grandeur
- Bird's eye view at conclusion

### Command
```powershell
python heart_animation.py --effect F --resolution large --density medium
```

---

## Effect G: Figure-8 Dance

**Duration:** 30 seconds  
**Complexity:** High  
**Best For:** Artistic videos, hypnotic effects

### Description
The camera follows a figure-8 (lemniscate) path around the rotating heart with synchronized zoom pulsing. Creates a mesmerizing, flowing motion.

### Technical Details
- **Heart Rotation:** 360° around Y-axis
- **Camera Path:** Lemniscate (∞ shape)
- **Horizontal Component:** ±60° azimuth oscillation
- **Vertical Component:** ±30° elevation oscillation (2x frequency)
- **Background Orbit:** 180° slow rotation
- **Zoom Pulse:** 20 ± 4 (synchronized with path)

### Visual Characteristics
- Infinity symbol motion path
- Vertical oscillation at double frequency
- Creates elegant, flowing curves
- Synchronized zoom enhances rhythm
- Hypnotic, artistic effect

### Command
```powershell
python heart_animation.py --effect G --resolution large --density medium
```

---

## Effect G1: Heart Journey

**Duration:** 90 seconds  
**Complexity:** Epic  
**Best For:** Long-form content, cinematic videos

### Description
An epic 90-second journey that rapidly zooms through the heart's center, exits behind it, then orbits back like a moon for 60 seconds. A dramatic narrative structure.

### Technical Details

### Phase 1: Rapid Approach (0-20s)
- **Zoom:** 150 → -10 (through heart center)
- **Acceleration:** Quadratic speed increase
- **Elevation:** 10° to 20° with sinusoidal variation
- **Azimuth:** Fixed at 45°

### Phase 2: Turnaround (20-30s)
- **Zoom:** -10 → 40 (exit and pull back)
- **Rotation:** 180° swing to opposite side
- **Elevation:** Fixed at 20°

### Phase 3: Orbital Return (30-90s, 60 seconds)
- **Orbit:** 2 complete revolutions (720°)
- **Zoom:** 40 → 25 (gradual approach)
- **Elevation:** ±25° oscillation (2 cycles)
- **Pattern:** Moon-like orbital motion

### Visual Characteristics
- Thrilling through-heart zoom
- Cinematic turnaround behind heart
- Long orbital sequence reveals all angles
- Two-phase structure: action + observation
- Perfect for extended viewing

### Command
```powershell
python heart_animation.py --effect G1 --resolution large --density low --output outputs/heart_journey.mp4
```

---

## Effect G2: Epic Heart Story

**Duration:** 137 seconds (2 minutes 17 seconds)  
**Complexity:** Cinematic  
**Best For:** YouTube videos, professional presentations, storytelling

### Description
The ultimate cinematic experience with 13 distinct phases including fade effects, formula displays, multiple through-heart zooms, distant perspectives, dramatic zoom-ins, close orbital sequences, and fade to black. A complete narrative arc.

### Technical Details

### Phase 1: Fade In (0-1s)
- **Effect:** Fade from black
- **Alpha:** 0 → 0.8
- **Zoom:** 12 (close, heart fills ~50% screen)
- **Position:** Frontal view

### Phase 2: Gradual Reveal (1-3s)
- **Zoom:** 80 → 12 (approach from distance)
- **Elevation:** 10° → 20°
- **Alpha:** 0.8 (full visibility)

### Phase 3: First Journey (3-60s, 57 seconds)
Condensed G1 effect:
- **0-20s:** Zoom through heart (12 → -10)
- **20-30s:** Exit and turnaround (-10 → 12, rotate 180°)
- **30-60s:** Begin orbital motion (12 → 10, 360° orbit)

### Phase 4: Fade Out (60-62s)
- **Alpha:** 0.8 → 0
- **Zoom:** 10 (heart disappears)

### Phase 5-6: Formula Display (62-66s)
- **Alpha:** 0 (heart invisible)
- **Display:** Parametric equations shown on black screen
- **Duration:** 4 seconds for reading

### Phase 7: Fade Back In (66-68s)
- **Alpha:** 0 → 0.8
- **Zoom:** 30 (medium distance)
- **Preparation:** Reset for second act

### Phase 8: Second Zoom Through (68-90s, 22 seconds)
- **Zoom:** 30 → -20 (accelerated through-heart)
- **Elevation:** 15° + 15° sinusoidal arc
- **Azimuth:** 45° → 135° (90° rotation)
- **Speed:** Faster than Phase 3

### Phase 9: Exit Behind (90-92s)
- **Zoom:** -20 → 15 (quick pullback)
- **Elevation:** 30° (higher angle)
- **Azimuth:** Complete 180° turn (135° → 225°)

### Phase 10: Distant Zoom Out (92-102s, 10 seconds)
- **Zoom:** 15 → 65 (heart becomes small)
- **Elevation:** 30° → 20° (descend)
- **Azimuth:** 225° → 405° (180° continued rotation)
- **Effect:** Heart in cosmic space

### Phase 11: Dramatic Zoom In (102-122s, 20 seconds)
- **Zoom:** 65 → 10 (quadratic acceleration)
- **Elevation:** Dramatic arc (20° ± 25°)
- **Azimuth:** 405° → 675° (270° rotation)
- **Effect:** Thrilling rush toward heart

### Phase 12: Moon Orbit (122-132s, 10 seconds)
- **Orbit:** 2 complete revolutions (720°)
- **Zoom:** 10 ± 4 (pulsing, very close)
- **Elevation:** ±15° (2 oscillations)
- **Effect:** Heart fills ~50% screen height
- **Best For:** Mobile viewing

### Phase 13: Final Fade Out (132-137s)
- **Zoom:** 10 → 70 (quadratic acceleration out)
- **Alpha:** 0.8 → 0 (fade to black)
- **Elevation:** 25° → 0° (return to neutral)
- **Azimuth:** Final 180° rotation

### Overall Heart Rotation
- **Total:** 270° over entire 137 seconds
- **Speed:** Slow, allowing phases to dominate

### Visual Characteristics
- Complete narrative structure with beginning, middle, end
- Multiple dramatic moments (zooms, fades, reveals)
- Formula display adds educational value
- Varied pacing: action, calm, action
- Close-up moon orbit perfect for mobile screens
- Professional fade in/out effects
- Ideal for YouTube with music overlay

### Recommended Settings
```powershell
# Standard quality (faster render)
python heart_animation.py --effect G2 --resolution large --density lower --fps 30 --output outputs/epic_heart_story.mp4

# 2x speed for YouTube (68.5 seconds, recommended)
python heart_animation.py --effect G2 --resolution 4k --density lower --fps 60 --bitrate 20000 --output outputs/heart_epic_story_2x.mp4

# Add audio with fade-out
ffmpeg -i outputs/heart_epic_story_2x.mp4 -i Engima.mp3 -t 68.5 -af "afade=t=out:st=66.5:d=2" -c:v copy -c:a aac -b:a 192k outputs/heart_epic_story_2x-sound.mp4
```

### Production Script
```powershell
.\scripts\build_g2_x2.ps1
```
Automatically generates G2 at 4K, 60 fps with audio integration.

---

## Comparison Table

| Effect | Duration | Complexity | Heart Rotation | Camera Motion | Zoom Changes | Special Features |
|--------|----------|------------|----------------|---------------|--------------|------------------|
| **A** | 30s | Simple | 360° Y-axis | Fixed | None | X-axis wobble |
| **B** | 30s | Simple | None | 360° orbit | None | Elevation oscillation |
| **C** | 30s | Moderate | 360° Y-axis | 180° orbit | In/Out | All combined |
| **D** | 30s | Moderate | 360° Y-axis | Elevation sweep | Pulse (4x) | Breathing effect |
| **E** | 30s | Moderate | 360° Y-axis | Wobble | None | Heartbeat pulse, scaling |
| **F** | 30s | High | 360° Y-axis | Spiral ascent | Gradual out | 720° orbit, -10° to 60° |
| **G** | 30s | High | 360° Y-axis | Figure-8 path | Pulse | Lemniscate motion |
| **G1** | 90s | Epic | 180° Y-axis | Through + orbit | Through heart | 3-phase journey |
| **G2** | 137s | Cinematic | 270° Y-axis | Multi-phase | Multiple | 13 phases, fades, formulas |

---

## Rendering Time Estimates

Based on typical hardware (varies by system):

| Effect | Small/Lower | Medium/Low | Large/Medium | 4K/Low |
|--------|-------------|------------|--------------|---------|
| A-D | 2-5 min | 8-15 min | 25-40 min | 50-90 min |
| E-G | 3-7 min | 10-18 min | 30-50 min | 60-100 min |
| G1 | 8-15 min | 25-45 min | 75-120 min | 150-270 min |
| G2 | 12-25 min | 40-70 min | 120-200 min | 240-360 min |

---

## Usage Examples

### Quick Test
```powershell
python heart_animation.py --effect A --resolution small --density lower
```

### High Quality Single Effect
```powershell
python heart_animation.py --effect E --resolution large --density medium --output outputs/heartbeat.mp4
```

### YouTube Production (Recommended)
```powershell
# Generate G2 at 2x speed (60 fps) in 4K
.\scripts\build_g2_x2.ps1

# Result: 68.5-second video with audio, ready for upload
```

### Batch Render Multiple Effects
```powershell
.\scripts\build_effects.ps1
```

### Custom Quality
```powershell
# 4K with high bitrate
python heart_animation.py --effect G2 --resolution 4k --bitrate 20000 --density low --output outputs/epic_4k.mp4

# Fast render for testing
python heart_animation.py --effect G --resolution small --density lower --dpi 80 --output outputs/test.mp4
```

---

## Choosing the Right Effect

### For Quick Demos
- **Effect A** or **B**: Simple, fast rendering

### For Presentations
- **Effect C** or **D**: Professional, dynamic

### For Artistic/Creative Content
- **Effect E**: Heartbeat theme
- **Effect F**: Dramatic spiral
- **Effect G**: Hypnotic figure-8

### For YouTube/Long-Form Content
- **Effect G1**: 90-second journey (fast-paced)
- **Effect G2**: 137-second epic story (cinematic)

### For Social Media
- **Effect E** (30s): Perfect for Instagram/TikTok
- **Effect G2 at 2x** (68.5s): Ideal for YouTube Shorts

### For Mobile Viewing
- **Effect G2**: Optimized with close zoom (heart fills 50% screen)
- Use lower density for faster loads

---

## Technical Notes

### Zoom Factor
- **Smaller values** = Closer camera = Bigger heart
- **G2 optimized**: Default zoom of 10-12 fills ~50% screen height
- **Standard effects**: Default zoom of 20

### Frame Rate
- **30 fps**: Standard, smooth playback
- **60 fps**: Use for 2x speed (plays back at 30 fps = 2x faster)

### Density vs Quality
- **Lower (~5K points)**: Fast rendering, good for testing/mobile
- **Low (10K points)**: Balanced quality and speed
- **Medium (22.5K points)**: High quality, slower render
- **High (40K points)**: Maximum quality, very slow

### Resolution Recommendations
- **Small (480p)**: Testing only
- **Medium (720p)**: Social media, fast turnaround
- **Large (1080p)**: YouTube standard, professional
- **4K (2160p)**: Premium content, future-proof

---

## Related Files

- **Main Script:** `heart_animation.py`
- **Build Scripts:** `scripts/build_effects.ps1`, `scripts/build_g2_x2.ps1`
- **Documentation:** `README.md`
- **YouTube Description:** `descriptions-heart_epic_story.txt`

---

## Contributing

To add new effects:

1. Add effect logic in `heart_animation.py` `update()` function
2. Update argument parser choices
3. Add effect name to `effect_names` dictionary
4. Document in this file
5. Update `README.md` with examples

---

**Last Updated:** November 14, 2025  
**Version:** 1.0 with G2 optimization (larger heart for mobile)

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
- [Effect H1: Heart Genesis](#effect-h1-heart-genesis)
- [Effect H2: Time Reversal](#effect-h2-time-reversal)
- [Effect H3: Fractal Heart](#effect-h3-fractal-heart)
- [Effect H4: Dual Hearts](#effect-h4-dual-hearts)
- [Effect H5: Kaleidoscope Heart](#effect-h5-kaleidoscope-heart)
- [Effect H6: Heart Nebula](#effect-h6-heart-nebula)
- [Effect H7: Hologram Heart](#effect-h7-hologram-heart)
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

## Effect H1: Heart Genesis

**Duration:** 100 seconds (1 minute 40 seconds)  
**Complexity:** Epic  
**Best For:** Opening sequences, creation stories, philosophical content

### Description
A creation story that begins with empty black space and a single point of light, which explodes into particles that gradually form the heart shape. The heart materializes, pulses to life, rotates majestically, then zooms out to cosmic scale. A complete narrative of birth and existence.

### Technical Details

### Phase 1: Empty Space (0-10s)
- **Heart:** Invisible (alpha: 0)
- **Zoom:** 200 (very far, cosmic scale)
- **Effect:** Black space with potential for single light point

### Phase 2: Particle Explosion (10-25s)
- **Alpha:** 0 → 0.8 (fade in)
- **Scale:** 0.1 → 1.0 (grows from tiny to normal)
- **Zoom:** 25 → 20 (approach)
- **Effect:** Particles coalesce into heart shape

### Phase 3: Materialization (25-40s)
- **Alpha:** 0.8 (fully visible)
- **Zoom:** 20 → 17 (continue approaching)
- **Elevation:** 20° ± 10° (sinusoidal sweep)
- **Azimuth:** 45° → 135° (90° rotation)
- **Effect:** Heart becomes solid and defined

### Phase 4: First Heartbeat (40-60s)
- **Heartbeat Pulse:** Scale 1.0 → 1.2 (20% expansion)
- **Pulse Frequency:** 2 beats per 20 seconds
- **Zoom:** 17 (constant, close view)
- **Azimuth:** 135° → 315° (180° rotation)
- **Effect:** Heart "comes to life" with rhythmic pulsing

### Phase 5: Majestic Rotation (60-75s)
- **Zoom:** 17 ± 3 (subtle pulsing)
- **Elevation:** 20° ± 20° (dramatic sweep)
- **Azimuth:** 315° → 675° (360° full rotation)
- **Effect:** Showcase heart's beauty from all angles

### Phase 6: Cosmic Scale (75-90s)
- **Alpha:** 0.8 → 1.0 (glow effect, brighter)
- **Zoom:** 20 → 100 (zoom out dramatically)
- **Elevation:** 40° → 20° (descend)
- **Azimuth:** 675° → 765° (90° rotation)
- **Effect:** Heart becomes star-like in cosmic space

### Phase 7: Blueprint of Creation (90-95s)
- **Alpha:** 1.0 (fully bright)
- **Zoom:** 100 (cosmic distance)
- **Display:** Formulas visible (if enabled)
- **Effect:** Mathematical foundation revealed

### Phase 8: Fade to Stars (95-100s)
- **Alpha:** 1.0 → 0 (fade out)
- **Zoom:** 100 → 200 (zoom out further)
- **Effect:** Heart fades, becomes one of infinite stars

### Overall Heart Rotation
- **Total:** 180° over entire 100 seconds
- **Speed:** Slow, allowing phases to dominate

### Visual Characteristics
- Complete creation narrative (nothing → something)
- Particle-like formation effect
- First heartbeat moment creates emotional impact
- Cosmic scale reveals heart as celestial body
- Formula display adds mathematical beauty
- Perfect for opening sequences or philosophical content

### Command
```powershell
python heart_animation.py --effect H1 --resolution large --density lower --formulas --output outputs/heart_genesis.mp4
```

---

## Effect H2: Time Reversal

**Duration:** 90 seconds  
**Complexity:** High  
**Best For:** Philosophical content, mind-bending visuals, artistic videos

### Description
A journey that plays forward for 45 seconds, freezes at a peak moment, then reverses completely. The heart and camera movements play backward, creating a mesmerizing time-echo effect that challenges perception.

### Technical Details

### Phase 1: Forward Journey (0-45s)
- **Heart Rotation:** 270° around Y-axis
- **Camera Motion:** Dynamic orbit with elevation changes
- **Zoom:** 20 → 10 → 20 (oscillating pattern)
- **Elevation:** 20° ± 15° (sinusoidal)
- **Azimuth:** 45° → 405° (360° orbit)
- **Effect:** Normal forward progression

### Phase 2: Freeze Frame (45-48s)
- **Heart:** Frozen at peak position
- **Zoom:** 15 (close view)
- **Elevation:** 35° (dramatic angle)
- **Azimuth:** 405° (peak position)
- **Effect:** Moment of suspension, anticipation

### Phase 3: Time Reversal (48-90s)
- **Heart Rotation:** Reverses from 270° back to 0°
- **Camera Motion:** All movements play backward
- **Zoom:** Reverses pattern (20 → 10 → 20)
- **Elevation:** Reverses oscillation
- **Azimuth:** Reverses orbit (405° → 45°)
- **Effect:** Everything moves backward in time

### Visual Characteristics
- Forward motion creates narrative
- Freeze frame adds dramatic pause
- Reversal creates "time echo" effect
- Mind-bending visual experience
- Philosophical implications of time
- Perfect for artistic or conceptual content

### Command
```powershell
python heart_animation.py --effect H2 --resolution large --density lower --output outputs/time_reversal.mp4
```

---

## Effect H3: Fractal Heart

**Duration:** 90 seconds  
**Complexity:** Epic  
**Best For:** Mathematical content, infinity themes, mind-expanding visuals

### Description
A journey into infinity: start with a normal heart, zoom deep into its center to discover smaller hearts within, continue zooming to find even smaller hearts, then zoom back out through all levels. The final reveal shows the universe is made of hearts.

### Technical Details

### Phase 1: Normal Heart (0-15s)
- **Zoom:** 20 (standard view)
- **Elevation:** 20° (standard angle)
- **Azimuth:** 45° → 225° (180° rotation)
- **Effect:** Establish baseline heart

### Phase 2: First Zoom In (15-45s)
- **Zoom:** 20 → 2 (dramatic zoom in)
- **Scale:** 1.0 → 0.5 (heart appears to shrink)
- **Elevation:** 20° ± 10° (oscillating)
- **Azimuth:** 225° → 585° (360° rotation)
- **Effect:** Discover smaller heart inside

### Phase 3: Deeper Zoom (45-60s)
- **Zoom:** 2 → 0.5 (extreme close-up)
- **Scale:** 0.5 → 0.2 (even smaller)
- **Elevation:** 30° ± 10° (more dramatic)
- **Azimuth:** 585° → 945° (360° rotation)
- **Effect:** Find third level of hearts

### Phase 4: Zoom Back Out (60-75s)
- **Zoom:** 0.5 → 20 (reverse journey)
- **Scale:** 0.2 → 1.0 (return to normal)
- **Elevation:** 40° → 20° (descend)
- **Azimuth:** 945° → 225° (reverse rotation)
- **Effect:** Travel back through all levels

### Phase 5: Cosmic Reveal (75-90s)
- **Zoom:** 20 → 50 (zoom out to cosmic scale)
- **Scale:** 1.0 (normal size)
- **Elevation:** 20° (neutral)
- **Azimuth:** 225° → 405° (180° rotation)
- **Effect:** Heart is one of many in infinite universe

### Visual Characteristics
- Recursive structure (heart within heart)
- Zoom creates sense of infinite depth
- Mathematical beauty of fractals
- Mind-expanding concept
- Perfect for math-oriented channels
- Visual metaphor for infinity

### Command
```powershell
python heart_animation.py --effect H3 --resolution large --density lower --output outputs/fractal_heart.mp4
```

---

## Effect H4: Dual Hearts

**Duration:** 120 seconds (2 minutes)  
**Complexity:** Epic  
**Best For:** Love stories, Valentine's Day, relationship content, emotional narratives

### Description
A love story told through two hearts: the first heart appears, then a second heart joins it. They orbit each other like binary stars, spiral closer together, briefly merge in an emotional peak, separate but remain connected, then perform a final synchronized orbit before fading.

### Technical Details

### Phase 1: First Heart Appears (0-15s)
- **Hearts:** Only heart 1 visible
- **Alpha:** 0 → 0.8 (fade in)
- **Zoom:** 30 → 20 (approach)
- **Effect:** Introduction of first character

### Phase 2: Second Heart Appears (15-30s)
- **Hearts:** Both hearts visible
- **Alpha:** 0.8 (both fully visible)
- **Separation:** 8 units (side by side)
- **Zoom:** 20 (constant)
- **Azimuth:** 45° → 135° (90° rotation)
- **Effect:** Second character enters

### Phase 3: Binary Orbit (30-60s)
- **Orbit Radius:** 8 units
- **Motion:** Circular orbit around center
- **Zoom:** 25 (slightly wider to show both)
- **Elevation:** 20° ± 10° (oscillating)
- **Azimuth:** 135° → 495° (360° orbit)
- **Effect:** Hearts dance around each other

### Phase 4: Spiral Closer (60-75s)
- **Orbit Radius:** 8 → 0 (spiral in)
- **Motion:** Tightening spiral
- **Zoom:** 20 → 15 (zoom in)
- **Elevation:** 30° → 20° (descend)
- **Azimuth:** 495° → 675° (180° rotation)
- **Effect:** Hearts drawn together

### Phase 5: Merge/Overlap (75-85s)
- **Position:** Hearts at same location
- **Alpha:** 0.8 → 1.0 (pulsing, brighter)
- **Pulse:** 4 pulses per 10 seconds
- **Zoom:** 15 (close view)
- **Azimuth:** 675° → 765° (90° rotation)
- **Effect:** Emotional peak, union

### Phase 6: Separation with Connection (85-95s)
- **Separation:** 0 → 4 units (move apart)
- **Alpha:** 0.8 (return to normal)
- **Zoom:** 15 → 20 (zoom out slightly)
- **Azimuth:** 765° → 855° (90° rotation)
- **Effect:** Separate but connected

### Phase 7: Synchronized Orbit (95-105s)
- **Orbit Radius:** 4 → 8 units (expand)
- **Motion:** Perfect synchronized orbit
- **Zoom:** 20 (constant)
- **Elevation:** 20° ± 5° (subtle oscillation)
- **Azimuth:** 855° → 1215° (360° orbit)
- **Effect:** Harmonious dance

### Phase 8: Fade to Black (105-120s)
- **Alpha:** 0.8 → 0 (fade out)
- **Orbit Radius:** 8 units (maintain)
- **Zoom:** 20 → 30 (zoom out)
- **Effect:** Connection remains visible as hearts fade

### Visual Characteristics
- Two-heart system creates narrative
- Binary star motion is visually striking
- Merge moment creates emotional peak
- Separation shows connection despite distance
- Perfect for love/relationship themes
- Universal emotional resonance

### Command
```powershell
python heart_animation.py --effect H4 --resolution large --density lower --output outputs/dual_hearts.mp4
```

---

## Effect H5: Kaleidoscope Heart

**Duration:** 60 seconds  
**Complexity:** High  
**Best For:** Artistic content, psychedelic visuals, mandala patterns, meditation videos

### Description
A mesmerizing kaleidoscope effect where a single heart multiplies through mirroring: first 4 quadrants, then 8 reflections, then 16 hearts forming a mandala pattern. The pattern then collapses back to reveal it was always one heart.

### Technical Details

### Phase 1: Single Heart (0-10s)
- **Hearts:** 1 (original)
- **Zoom:** 20 (standard view)
- **Elevation:** 20° (standard angle)
- **Azimuth:** 45° → 225° (180° rotation)
- **Effect:** Establish base heart

### Phase 2: 4 Quadrants (10-25s)
- **Hearts:** 4 (original + 3 mirrors)
- **Mirroring:** X-axis, Y-axis, both axes
- **Alpha:** 0 → 0.8 (fade in mirrors)
- **Zoom:** 25 (wider to show all)
- **Azimuth:** 225° → 405° (180° rotation)
- **Effect:** First multiplication

### Phase 3: 8 Reflections (25-40s)
- **Hearts:** 8 (octagon pattern)
- **Mirroring:** 45° increments around circle
- **Zoom:** 30 (even wider)
- **Elevation:** 20° ± 10° (oscillating)
- **Azimuth:** 405° → 765° (360° rotation)
- **Effect:** Mandala begins to form

### Phase 4: 16 Hearts (40-50s)
- **Hearts:** 16 (full mandala)
- **Mirroring:** 22.5° increments
- **Zoom:** 35 (maximum width)
- **Elevation:** 20° ± 15° (dramatic oscillation)
- **Azimuth:** 765° → 1485° (720° rotation)
- **Effect:** Complete kaleidoscope pattern

### Phase 5: Collapse (50-55s)
- **Hearts:** 16 → 1 (fade out mirrors)
- **Alpha:** 0.8 → 0 (fade out)
- **Zoom:** 35 → 20 (zoom in)
- **Elevation:** 35° → 20° (descend)
- **Azimuth:** 1485° → 45° (reverse rotation)
- **Effect:** Pattern dissolves

### Phase 6: Final Reveal (55-60s)
- **Hearts:** 1 (original only)
- **Alpha:** 0 → 0.8 (fade back in)
- **Zoom:** 20 (standard)
- **Elevation:** 20° (neutral)
- **Azimuth:** 45° (starting position)
- **Effect:** Was always one heart

### Visual Characteristics
- Hypnotic mandala patterns
- Symmetrical beauty
- Multiplication creates visual complexity
- Collapse reveals unity
- Perfect for artistic/meditation content
- Psychedelic, trippy aesthetic

### Command
```powershell
python heart_animation.py --effect H5 --resolution large --density lower --output outputs/kaleidoscope_heart.mp4
```

---

## Effect H6: Heart Nebula

**Duration:** 120 seconds (2 minutes)  
**Complexity:** Epic  
**Best For:** Space themes, cosmic content, awe-inspiring visuals, science channels

### Description
A cosmic journey through deep space: start in the void with a distant glowing heart-nebula, travel through stars toward it, pass through cosmic dust, arrive at the massive glowing heart, orbit it like a planet, see other heart-planets in the distance, then zoom out to reveal the heart galaxy.

### Technical Details

### Phase 1: Deep Space (0-15s)
- **Alpha:** 0.3 → 0.8 (glow effect, fade in)
- **Zoom:** 200 → 50 (approach from cosmic distance)
- **Elevation:** 20° (neutral)
- **Azimuth:** 45° (frontal)
- **Effect:** Distant heart glows like galaxy

### Phase 2: Travel Through Stars (15-45s)
- **Alpha:** 0.8 ± 0.2 (pulsing glow)
- **Zoom:** 50 → 20 (continue approaching)
- **Elevation:** 20° ± 10° (oscillating)
- **Azimuth:** 45° → 225° (180° rotation)
- **Effect:** Journey through starfield

### Phase 3: Cosmic Dust (45-60s)
- **Alpha:** 0.8 ± 0.2 (rapid pulsing)
- **Zoom:** 20 → 15 (get very close)
- **Elevation:** 30° → 20° (descend)
- **Azimuth:** 225° → 315° (90° rotation)
- **Effect:** Pass through particle field

### Phase 4: Arrival (60-75s)
- **Alpha:** 1.0 (fully bright, glowing)
- **Zoom:** 15 ± 2 (close, pulsing)
- **Elevation:** 20° ± 15° (dramatic arc)
- **Azimuth:** 315° → 495° (180° rotation)
- **Effect:** Heart is massive and glowing

### Phase 5: Orbital Motion (75-90s)
- **Alpha:** 1.0 (fully bright)
- **Zoom:** 17 (constant, close orbit)
- **Elevation:** 20° ± 25° (2 oscillations)
- **Azimuth:** 495° → 855° (360° orbit)
- **Effect:** Orbit around heart-planet

### Phase 6: Distant Hearts (90-105s)
- **Alpha:** 1.0 (fully bright)
- **Zoom:** 17 → 37 (zoom out to see others)
- **Elevation:** 45° → 20° (descend)
- **Azimuth:** 855° → 1035° (180° rotation)
- **Effect:** See other heart-planets

### Phase 7: Galaxy View (105-120s)
- **Alpha:** 1.0 → 0.8 (slight fade)
- **Zoom:** 37 → 200 (zoom out dramatically)
- **Elevation:** 20° (neutral)
- **Azimuth:** 1035° → 1125° (90° rotation)
- **Effect:** Heart is one of many in galaxy

### Overall Heart Rotation
- **Total:** 180° over entire 120 seconds
- **Speed:** Slow, allowing cosmic journey to dominate

### Visual Characteristics
- Cosmic scale creates awe
- Glow effects make heart celestial
- Journey structure creates narrative
- Orbital motion shows heart as planet
- Galaxy view reveals infinite hearts
- Perfect for space/science content

### Command
```powershell
python heart_animation.py --effect H6 --resolution large --density lower --output outputs/heart_nebula.mp4
```

---

## Effect H7: Hologram Heart

**Duration:** 90 seconds  
**Complexity:** High  
**Best For:** Tech content, sci-fi themes, futuristic aesthetics, cyberpunk visuals

### Description
A futuristic holographic projection: grid floor appears, heart materializes as wireframe, fills in progressively, glitches and reforms, shows multiple holographic layers, displays scan lines, then powers down in sections. A complete tech aesthetic experience.

### Technical Details

### Phase 1: Grid Appearance (0-10s)
- **Heart:** Invisible (alpha: 0)
- **Zoom:** 30 (medium distance)
- **Elevation:** 20° (standard)
- **Azimuth:** 45° (frontal)
- **Effect:** Tron-style grid environment

### Phase 2: Wireframe Materialization (10-20s)
- **Alpha:** 0 → 0.3 (wireframe effect, low opacity)
- **Zoom:** 30 → 20 (approach)
- **Elevation:** 20° (constant)
- **Azimuth:** 45° → 135° (90° rotation)
- **Effect:** Heart appears as wireframe

### Phase 3: Progressive Fill (20-35s)
- **Alpha:** 0.3 → 0.8 (gradually fill in)
- **Zoom:** 20 (constant)
- **Elevation:** 20° ± 10° (oscillating)
- **Azimuth:** 135° → 315° (180° rotation)
- **Effect:** Wireframe becomes solid

### Phase 4: Glitch Effects (35-50s)
- **Alpha:** 0.8 ± 0.1 (glitch fluctuations)
- **Glitch Pattern:** Complex sinusoidal interference
- **Zoom:** 20 ± 3 (pulsing)
- **Elevation:** 30° ± 10° (oscillating)
- **Azimuth:** 315° → 675° (360° rotation)
- **Effect:** Hologram glitches and reforms

### Phase 5: Multiple Layers (50-70s)
- **Alpha:** 0.8 ± 0.2 (layer effect)
- **Zoom:** 17 ± 3 (pulsing)
- **Elevation:** 20° ± 20° (dramatic sweep)
- **Azimuth:** 675° → 1215° (540° rotation)
- **Effect:** X-ray-like layered views

### Phase 6: Scan Lines (70-85s)
- **Alpha:** 1.0 ± 0.1 (scan line effect)
- **Scan Pattern:** High-frequency oscillation
- **Zoom:** 20 (constant)
- **Elevation:** 40° → 20° (descend)
- **Azimuth:** 1215° → 1395° (180° rotation)
- **Effect:** Final solid form with tech aesthetic

### Phase 7: Power Down (85-90s)
- **Alpha:** 1.0 → 0 (fade out)
- **Zoom:** 20 → 30 (zoom out)
- **Elevation:** 20° (neutral)
- **Azimuth:** 1395° (final position)
- **Effect:** Hologram deactivates

### Overall Heart Rotation
- **Total:** 360° over entire 90 seconds
- **Speed:** Moderate, allowing tech effects to show

### Visual Characteristics
- Futuristic tech aesthetic
- Wireframe to solid progression
- Glitch effects add authenticity
- Scan lines create hologram feel
- Perfect for sci-fi/tech content
- Cyberpunk visual style

### Command
```powershell
python heart_animation.py --effect H7 --resolution large --density lower --output outputs/hologram_heart.mp4
```

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
| **H1** | 100s | Epic | 180° Y-axis | Multi-phase | Multiple | Creation story, particle effects, cosmic scale |
| **H2** | 90s | High | 270° Y-axis | Forward + reverse | Oscillating | Time reversal, freeze frame |
| **H3** | 90s | Epic | 360° Y-axis | Deep zoom | Extreme in/out | Fractal hearts, recursive structure |
| **H4** | 120s | Epic | 360° Y-axis | Dual orbit | Multiple | Two hearts, binary motion, merge |
| **H5** | 60s | High | 360° Y-axis | Multi-mirror | Expanding | Kaleidoscope, mandala patterns |
| **H6** | 120s | Epic | 180° Y-axis | Cosmic journey | Multiple | Space theme, glow effects, galaxy view |
| **H7** | 90s | High | 360° Y-axis | Tech aesthetic | Pulsing | Hologram, wireframe, glitch effects |

---

## Rendering Time Estimates

Based on typical hardware (varies by system):

| Effect | Small/Lower | Medium/Low | Large/Medium | 4K/Low |
|--------|-------------|------------|--------------|---------|
| A-D | 2-5 min | 8-15 min | 25-40 min | 50-90 min |
| E-G | 3-7 min | 10-18 min | 30-50 min | 60-100 min |
| G1 | 8-15 min | 25-45 min | 75-120 min | 150-270 min |
| G2 | 12-25 min | 40-70 min | 120-200 min | 240-360 min |
| H1 | 10-20 min | 35-60 min | 100-160 min | 200-360 min |
| H2 | 8-15 min | 25-45 min | 75-120 min | 150-270 min |
| H3 | 8-15 min | 25-45 min | 75-120 min | 150-270 min |
| H4 | 12-25 min | 40-70 min | 120-200 min | 240-360 min |
| H5 | 5-10 min | 15-30 min | 45-75 min | 90-150 min |
| H6 | 12-25 min | 40-70 min | 120-200 min | 240-360 min |
| H7 | 8-15 min | 25-45 min | 75-120 min | 150-270 min |

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
# Render all A-G effects
.\scripts\build_effects.ps1

# Render all H* effects at large resolution
.\scripts\build_h_large.ps1
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
- **Effect H1**: 100-second creation story (philosophical)
- **Effect H4**: 120-second love story (emotional)
- **Effect H6**: 120-second cosmic journey (awe-inspiring)

### For Social Media
- **Effect E** (30s): Perfect for Instagram/TikTok
- **Effect G2 at 2x** (68.5s): Ideal for YouTube Shorts
- **Effect H5** (60s): Kaleidoscope for artistic content
- **Effect H7** (90s): Hologram for tech/sci-fi channels

### For Special Themes
- **Effect H1**: Creation/philosophy themes
- **Effect H2**: Time/philosophy themes
- **Effect H3**: Math/infinity themes
- **Effect H4**: Love/relationship themes
- **Effect H5**: Art/meditation themes
- **Effect H6**: Space/science themes
- **Effect H7**: Tech/sci-fi themes

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
- **Build Scripts:** 
  - `scripts/build_effects.ps1` (A-G effects)
  - `scripts/build_g2_x2.ps1` (G2 with audio)
  - `scripts/build_h_large.ps1` (H* effects at large resolution)
- **Documentation:** `README.md`
- **YouTube Description:** `descriptions-heart_epic_story.txt`
- **Effect Concepts:** `TODO/TODO-effects-H.md`

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
**Version:** 2.0 with H* effects (H1-H7) - 7 new epic storytelling effects

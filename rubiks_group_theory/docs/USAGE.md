# Usage Guide

This guide explains how to use the Rubik's Cube Group Theory Solver application.

## Keyboard Controls

### Cube Moves

All moves can be performed clockwise or counter-clockwise:

| Key | Move | Description |
|-----|------|-------------|
| `U` | U | Rotate top face clockwise |
| `Shift+U` | U' | Rotate top face counter-clockwise |
| `D` | D | Rotate bottom face clockwise |
| `Shift+D` | D' | Rotate bottom face counter-clockwise |
| `R` | R | Rotate right face clockwise |
| `Shift+R` | R' | Rotate right face counter-clockwise |
| `L` | L | Rotate left face clockwise |
| `Shift+L` | L' | Rotate left face counter-clockwise |
| `F` | F | Rotate front face clockwise |
| `Shift+F` | F' | Rotate front face counter-clockwise |
| `B` | B | Rotate back face clockwise |
| `Shift+B` | B' | Rotate back face counter-clockwise |

### Application Controls

| Key | Action |
|-----|-------|
| `F11` | Toggle fullscreen mode |
| `V` | Switch between flat and graph visualization modes |
| `ESC` | Close application (via window close button) |

## Mouse Controls

### Solve Button

- **Location**: Top-right corner of the screen
- **Click**: Start the auto-solver
- **States**:
  - Normal: Ready to solve
  - Hover: Mouse over button (highlighted)
  - Disabled: Currently solving (grayed out)
  - Clicked: Button press feedback

## Visualization Modes

### Flat View (Default)

The standard "unfolded cross" layout:
```
     [Top]
[Back] [Left] [Front] [Right]
     [Bottom]
```

This view shows all 6 faces in a 2D layout, making it easy to see the entire cube state.

### Graph View

A planar graph representation where:
- Each of the 54 stickers is shown as a colored dot
- The graph structure represents the cube's connectivity
- Useful for understanding the group theory perspective

Press `V` to switch between modes.

## Using the Auto Solver

1. **Scramble the cube** (optional): Use keyboard controls to mix up the cube
2. **Click the "Solve" button**: Located in the top-right corner
3. **Watch the animation**: The solver will apply moves step-by-step
4. **Progress indicator**: Shows "Solving step X/Y" at the bottom of the screen
5. **Completion**: When solved, "SOLVED!" appears at the top

### Solver Behavior

- The solver uses the beginner's method (layer-by-layer)
- Moves are animated with a delay (default: 0.8 seconds per move)
- Keyboard controls are disabled while solving
- The button is disabled during solving to prevent interruption

## Window Management

### Resolution

- **Default**: 1920×1080 (16:9 aspect ratio)
- **Alternative**: 1280×720 (HD, 16:9)
- The window maintains 16:9 aspect ratio when resized

### Fullscreen Mode

- Press `F11` to toggle fullscreen
- In fullscreen, the application uses your native screen resolution
- All UI elements scale proportionally
- Press `F11` again to return to windowed mode

### Resizing

- The window is resizable in windowed mode
- Aspect ratio is automatically maintained
- Cube visualization scales to fit the window size

## Understanding the Display

### Color Scheme

The cube uses a custom color palette:
- **White (W)**: bookwhite
- **Yellow (Y)**: warmstone
- **Red (R)**: bookred
- **Orange (O)**: lawpurple
- **Blue (B)**: bookpurple
- **Green (G)**: Complementary green

### Status Indicators

- **"SOLVED!" text**: Appears when the cube is in a solved state
- **Progress text**: Shows solving progress during auto-solve
- **Button state**: Visual feedback for button interactions

## Tips for Manual Solving

1. **Start with the white cross**: Position white edges on the bottom face
2. **Solve white corners**: Complete the bottom layer
3. **Middle layer**: Position middle layer edges
4. **Yellow cross**: Create the yellow cross on top
5. **Orient corners**: Fix yellow corner orientations
6. **Final permutation**: Position yellow corners correctly

For detailed algorithm explanations, see [algorithms.md](algorithms.md).

## Troubleshooting

### Cube Not Responding
- Check that the application window has focus
- Ensure you're not in the middle of a solve animation
- Try clicking the window to regain focus

### Solver Not Working
- Make sure the cube is in a valid state
- The solver works best from scrambled states
- If stuck, try scrambling and solving again

### Display Issues
- Try toggling fullscreen (F11)
- Switch visualization modes (V)
- Resize the window to refresh the layout

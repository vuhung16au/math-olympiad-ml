# Rubik's Cube 2D Group Theory Solver

A Python application that visualizes and solves Rubik's Cube using group theory principles, with Pygame-based 2D visualization.

## Overview

This project combines abstract mathematics (Group Theory), solving algorithms, and visual representation to create an interactive Rubik's Cube solver. The cube is represented using permutation-based group theory, allowing for pure mathematical manipulation separate from visualization.

## Features

- **Group Theory Representation**: Cube moves are implemented as permutations of 54 stickers
- **Dual Visualization Modes**:
  - Flat renderer: Standard "unfolded cross" view
  - Graph renderer: Planar graph representation (foundation)
- **Auto Solver**: Beginner's method (layer-by-layer) solver with step-by-step animation
- **Interactive Controls**: Keyboard controls for all 12 basic moves
- **Custom Color Palette**: Beautiful, consistent color scheme
- **16:9 Resolution Support**: Fullscreen mode with aspect ratio preservation

## Architecture

The project is organized into modular components:

- **`core/`**: Pure mathematical logic (cube state, permutations)
- **`visualization/`**: Pygame rendering code (flat and graph views)
- **`solvers/`**: Solving algorithms (beginner's method)
- **`docs/`**: Documentation and guides

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for installation and running instructions.

## Documentation

- [QUICKSTART.md](QUICKSTART.md) - Build and run instructions
- [docs/USAGE.md](docs/USAGE.md) - User guide and controls
- [docs/algorithms.md](docs/algorithms.md) - Algorithm descriptions and group theory concepts
- [docs/TODO.md](docs/TODO.md) - Future enhancements

## Requirements

- Python 3.8+
- pygame 2.5.0+
- uv (for package management)

## License

This project is provided as-is for educational purposes.

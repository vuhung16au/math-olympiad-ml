# Quick Start Guide

This guide will help you set up and run the Rubik's Cube Group Theory Solver.

## Prerequisites

- Python 3.8 or higher
- `uv` package manager

## Installing uv

If you don't have `uv` installed, you can install it using one of these methods:

### Using pip
```bash
pip install uv
```

### Using curl (Linux/macOS)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Using PowerShell (Windows)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, visit: https://github.com/astral-sh/uv

## Setting Up the Project

1. **Navigate to the project directory:**
   ```bash
   cd rubiks_group_theory
   ```

2. **Install dependencies using uv:**
   ```bash
   uv pip install -e .
   ```
   
   Or if you prefer to use a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. **(Optional) Enable fast Two-Phase solving (Kociemba):**
   ```bash
   uv pip install -e ".[fast-solver]"
   ```

## Running the Application

1. **If you're in a virtual environment, activate it first:**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies (if not already installed):**
   ```bash
   uv pip install pygame
   ```

3. **Start the application:**
   ```bash
   python main.py
   ```
   
   Or if using uv (may require package installation first):
   ```bash
   uv run main.py
   ```
   
   **Note**: If `uv run` gives permission errors, use `python main.py` directly after installing dependencies.

2. **The application window will open** showing the Rubik's Cube in the default flat view.

## First Steps

- **Rotate faces**: Use keyboard keys `U`, `D`, `R`, `L`, `F`, `B` for clockwise moves
- **Counter-clockwise moves**: Hold `Shift` while pressing the move key
- **Toggle fullscreen**: Press `F11`
- **Switch visualization**: Press `V` to toggle between flat and graph views
- **Solve the cube**: Click the "Solve" button in the top-right corner

## Troubleshooting

### Import Errors
If you encounter import errors, make sure you're running from the project root directory and that dependencies are installed:
```bash
uv pip install -e .
```

### Display Issues
If the window doesn't appear or has display issues:
- Check that pygame is properly installed: `uv pip list | grep pygame`
- Try running in windowed mode first (not fullscreen)
- Check your display resolution supports 16:9 aspect ratio

### Performance Issues
If the application runs slowly:
- Reduce the window size
- The solver animation delay can be adjusted in `main.py` (default: 800ms)

## Next Steps

- Read [docs/USAGE.md](docs/USAGE.md) for detailed usage instructions
- Explore [docs/algorithms.md](docs/algorithms.md) to understand the group theory approach
- Check [docs/TODO.md](docs/TODO.md) for planned enhancements

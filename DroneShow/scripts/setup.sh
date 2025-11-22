#!/bin/bash
# Setup script for drone show simulation
# Creates virtual environment and installs dependencies

set -e

echo "=========================================="
echo "Drone Show Simulation - Setup"
echo "=========================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed"
    echo "Please install uv first: https://github.com/astral-sh/uv"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -r requirements.txt

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the drone show:"
echo "  python drone_show.py"
echo ""


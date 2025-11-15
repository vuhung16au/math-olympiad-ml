#!/bin/bash
# MathHeart Player - Run Script for Linux/macOS
# This script activates the virtual environment and runs the application

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "Installing dependencies..."
    venv/bin/pip install --upgrade pip
    venv/bin/pip install -r mathheart_player/requirements.txt
fi

# Activate virtual environment and run
echo "Starting MathHeart Player..."
source venv/bin/activate
python mathheart_player/main.py


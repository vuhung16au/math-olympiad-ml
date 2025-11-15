# MathHeart Player - Run Script for Windows PowerShell
# This script activates the virtual environment and runs the application

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Virtual environment not found. Creating..."
    python -m venv venv
    Write-Host "Installing dependencies..."
    .\venv\Scripts\python.exe -m pip install --upgrade pip
    .\venv\Scripts\python.exe -m pip install -r mathheart_player/requirements.txt
}

# Activate virtual environment and run
Write-Host "Starting MathHeart Player..."
.\venv\Scripts\python.exe mathheart_player/main.py


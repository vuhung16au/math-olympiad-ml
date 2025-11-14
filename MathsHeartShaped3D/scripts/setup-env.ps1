# Setup Environment Script
# Initializes virtual environment using uv and installs requirements
# Usage: .\scripts\setup-env.ps1

# Define color output functions
function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Write-Section {
    param([string]$Message)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host $Message -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Yellow
}

# Display header
Write-Section "Python Environment Setup"
Write-Host ""

# Validate prerequisites
Write-Info "Validating prerequisites..."

# Check if uv is installed
try {
    $uvVersion = uv --version 2>&1
    Write-Success "✓ uv found: $uvVersion"
} catch {
    Write-Error-Custom "✗ uv not found. Please install uv first."
    Write-Info "Install uv with: pip install uv"
    Write-Info "Or visit: https://github.com/astral-sh/uv"
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Success "✓ Python found: $pythonVersion"
} catch {
    Write-Error-Custom "✗ Python not found. Please install Python first."
    exit 1
}

Write-Host ""

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Write-Error-Custom "✗ requirements.txt not found in current directory."
    exit 1
}
Write-Success "✓ requirements.txt found"

Write-Host ""

# Step 1: Initialize virtual environment
Write-Section "Step 1: Initializing Virtual Environment"
Write-Info "Creating virtual environment at .venv..."

if (Test-Path ".venv") {
    Write-Info "Virtual environment already exists. Removing old one..."
    Remove-Item -Recurse -Force ".venv"
}

try {
    uv venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✓ Virtual environment created successfully"
    } else {
        throw "uv venv returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Error-Custom "✗ Failed to create virtual environment: $_"
    exit 1
}

Write-Host ""

# Step 2: Install requirements
Write-Section "Step 2: Installing Requirements"
Write-Info "Installing packages from requirements.txt..."

try {
    uv pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✓ Requirements installed successfully"
    } else {
        throw "uv pip install returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Error-Custom "✗ Failed to install requirements: $_"
    exit 1
}

Write-Host ""

# Step 3: Activate virtual environment
Write-Section "Step 3: Activating Virtual Environment"
Write-Info "Activating virtual environment..."

$activateScript = ".\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Error-Custom "✗ Activation script not found: $activateScript"
    exit 1
}

try {
    & $activateScript
    Write-Success "✓ Virtual environment activated"
    Write-Host ""
    Write-Info "Virtual environment is now active. You can verify with:"
    Write-Host "  python --version" -ForegroundColor White
    Write-Host "  pip list" -ForegroundColor White
} catch {
    Write-Error-Custom "✗ Failed to activate virtual environment: $_"
    Write-Info "You can manually activate it with:"
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Section "Setup Complete"
Write-Success "✓ Environment setup completed successfully!"
Write-Host ""
Write-Info "Your virtual environment is ready to use."
Write-Host ""

exit 0


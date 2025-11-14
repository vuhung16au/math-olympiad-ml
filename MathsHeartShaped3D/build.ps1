# Build script for generating 3D heart animations
# Usage: .\build.ps1 [small|medium|large]

param(
    [Parameter(Position=0)]
    [ValidateSet('small', 'medium', 'large')]
    [string]$Size = 'medium'
)

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

# Display header
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "       3D Heart Animation Builder" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

# Validate Python is available
Write-Info "Checking Python installation..."
try {
    $pythonVersion = python --version 2>&1
    Write-Success "✓ Found: $pythonVersion"
} catch {
    Write-Error-Custom "✗ Python not found. Please install Python 3.12.10 or compatible version."
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Error-Custom "✗ Virtual environment not found."
    Write-Info "Please run the following commands to set up:"
    Write-Host "  uv venv .venv" -ForegroundColor White
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  uv pip install -r requirements.txt" -ForegroundColor White
    exit 1
}

# Check if virtual environment is activated
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error-Custom "✗ Virtual environment Python not found."
    exit 1
}

Write-Success "✓ Virtual environment found"

# Check FFmpeg
Write-Info "Checking FFmpeg installation..."
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Success "✓ FFmpeg found"
} catch {
    Write-Error-Custom "✗ FFmpeg not found. Please install FFmpeg and add it to PATH."
    Write-Info "Install with: winget install FFmpeg"
    exit 1
}

# Define output path
$outputPath = "outputs/heart_animation-$Size.mp4"

# Display build configuration
Write-Host ""
Write-Host "Build Configuration:" -ForegroundColor Yellow
Write-Host "  Resolution: $Size" -ForegroundColor White
Write-Host "  Output: $outputPath" -ForegroundColor White
Write-Host ""

# Estimate render time
$estimatedTime = switch ($Size) {
    'small'  { "5-10 minutes" }
    'medium' { "10-20 minutes" }
    'large'  { "20-40 minutes" }
}
Write-Info "Estimated render time: $estimatedTime"
Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Proceed with rendering? (Y/n)"
if ($confirm -eq 'n' -or $confirm -eq 'N') {
    Write-Host "Build cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Info "Starting animation generation..."
Write-Host ""

# Record start time
$startTime = Get-Date

# Run the Python script
& $venvPython heart_animation.py --resolution $Size --output $outputPath

# Check if the script succeeded
if ($LASTEXITCODE -eq 0) {
    $endTime = Get-Date
    $duration = $endTime - $startTime
    $minutes = [math]::Floor($duration.TotalMinutes)
    $seconds = [math]::Floor($duration.Seconds)
    
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Success "✓ Animation successfully generated!"
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Output: $outputPath" -ForegroundColor White
    Write-Host "  Resolution: $Size" -ForegroundColor White
    Write-Host "  Render time: $minutes minutes, $seconds seconds" -ForegroundColor White
    Write-Host ""
    
    # Check if file exists and show size
    if (Test-Path $outputPath) {
        $fileSize = (Get-Item $outputPath).Length / 1MB
        Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
    }
    
    Write-Host ""
    Write-Info "To view the video, open: $outputPath"
    
} else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Error-Custom "✗ Animation generation failed!"
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Info "Please check the error messages above for details."
    exit 1
}

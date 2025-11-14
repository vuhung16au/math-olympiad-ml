# Build H8 Effect with Audio
# Generates H8 effect video and combines it with audio
# Usage: .\scripts\h8.ps1

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
Write-Section "H8 Effect - Heart Genesis with Music Sync"
Write-Host ""
Write-Info "This script will:"
Write-Host "  1. Generate H8 effect video (outputs/h8.mp4)" -ForegroundColor White
Write-Host "  2. Copy video to inputs/h8.mp4" -ForegroundColor White
Write-Host "  3. Combine video with audio (inputs/H8InfiniteStars2.mp3)" -ForegroundColor White
Write-Host "  4. Save final video to outputs/h8-sound.mp4" -ForegroundColor White
Write-Host ""

# Validate prerequisites
Write-Info "Validating prerequisites..."

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "✓ Python found: $pythonVersion"
} catch {
    Write-Error-Custom "✗ Python not found. Please install Python 3.12.10 or compatible version."
    exit 1
}

# Check virtual environment
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error-Custom "✗ Virtual environment not found."
    Write-Info "Please run setup first:"
    Write-Host "  .\scripts\setup-env.ps1" -ForegroundColor White
    exit 1
}
Write-Success "✓ Virtual environment found"

# Check FFmpeg
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Success "✓ FFmpeg found"
} catch {
    Write-Error-Custom "✗ FFmpeg not found. Please install FFmpeg."
    exit 1
}

# Check if heart_animation.py exists
if (-not (Test-Path "heart_animation.py")) {
    Write-Error-Custom "✗ heart_animation.py not found in current directory."
    exit 1
}
Write-Success "✓ heart_animation.py found"

# Check if audio file exists
if (-not (Test-Path "inputs/H8InfiniteStars2.mp3")) {
    Write-Error-Custom "✗ inputs/H8InfiniteStars2.mp3 not found."
    Write-Info "Please ensure the audio file is present before running this script."
    exit 1
}
Write-Success "✓ inputs/H8InfiniteStars2.mp3 found"

Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Proceed with generating H8 effect and combining with audio? (Y/n)"
if ($confirm -eq 'n' -or $confirm -eq 'N') {
    Write-Host "Build cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# Create directories if they don't exist
if (-not (Test-Path "outputs")) {
    New-Item -ItemType Directory -Path "outputs" | Out-Null
    Write-Info "Created outputs directory"
}

if (-not (Test-Path "inputs")) {
    New-Item -ItemType Directory -Path "inputs" | Out-Null
    Write-Info "Created inputs directory"
}

# Step 1: Generate the video
Write-Section "Step 1: Generating H8 Animation"
Write-Host ""
Write-Info "Generating H8 effect at large resolution..."
Write-Info "Output: outputs/h8.mp4"
Write-Host ""

$videoStartTime = Get-Date

$videoCommand = "& `"$venvPython`" heart_animation.py --effect H8 --resolution large --density lower --output outputs/h8.mp4"

try {
    Invoke-Expression $videoCommand
    
    if ($LASTEXITCODE -eq 0) {
        $videoEndTime = Get-Date
        $videoDuration = $videoEndTime - $videoStartTime
        $minutes = [math]::Floor($videoDuration.TotalMinutes)
        $seconds = [math]::Floor($videoDuration.Seconds)
        
        Write-Host ""
        Write-Success "✓ Video generation completed successfully!"
        Write-Host "  Render time: $minutes minutes, $seconds seconds" -ForegroundColor White
        
        # Get file size
        if (Test-Path "outputs/h8.mp4") {
            $fileSize = (Get-Item "outputs/h8.mp4").Length / 1MB
            Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
        }
    } else {
        throw "Video generation returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Error-Custom "✗ Video generation failed: $_"
    exit 1
}

Write-Host ""

# Step 2: Copy video to inputs directory
Write-Section "Step 2: Copying Video to Inputs Directory"
Write-Host ""
Write-Info "Copying outputs/h8.mp4 to inputs/h8.mp4..."

try {
    Copy-Item -Path "outputs/h8.mp4" -Destination "inputs/h8.mp4" -Force
    Write-Success "✓ Video copied successfully"
} catch {
    Write-Host ""
    Write-Error-Custom "✗ Failed to copy video: $_"
    exit 1
}

Write-Host ""

# Step 3: Combine video with audio
Write-Section "Step 3: Combining Video with Audio"
Write-Host ""
Write-Info "Combining inputs/h8.mp4 with inputs/H8InfiniteStars2.mp3..."
Write-Info "Output: outputs/h8-sound.mp4"
Write-Host ""

$audioStartTime = Get-Date

# Get video duration for audio trimming (100 seconds = 1:40)
$audioCommand = "ffmpeg -i inputs/h8.mp4 -i inputs/H8InfiniteStars2.mp3 -t 100 -c:v copy -c:a aac -b:a 192k outputs/h8-sound.mp4"

try {
    Invoke-Expression $audioCommand
    
    if ($LASTEXITCODE -eq 0) {
        $audioEndTime = Get-Date
        $audioDuration = $audioEndTime - $audioStartTime
        $audioSeconds = [math]::Floor($audioDuration.TotalSeconds)
        
        Write-Host ""
        Write-Success "✓ Audio mixing completed successfully!"
        Write-Host "  Processing time: $audioSeconds seconds" -ForegroundColor White
        
        # Get file size
        if (Test-Path "outputs/h8-sound.mp4") {
            $fileSize = (Get-Item "outputs/h8-sound.mp4").Length / 1MB
            Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
        }
    } else {
        throw "Audio mixing returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Error-Custom "✗ Audio mixing failed: $_"
    Write-Info "Video without audio is available at: outputs/h8.mp4"
    exit 1
}

# Calculate total time
$totalEndTime = Get-Date
$totalDuration = $totalEndTime - $videoStartTime
$totalMinutes = [math]::Floor($totalDuration.TotalMinutes)
$totalSeconds = [math]::Floor($totalDuration.Seconds)

# Display final summary
Write-Section "Build Summary"
Write-Host ""
Write-Success "✓ H8 effect with audio completed successfully!"
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "  1. outputs/h8.mp4 (video only)" -ForegroundColor White
Write-Host "  2. inputs/h8.mp4 (copy of video)" -ForegroundColor White
Write-Host "  3. outputs/h8-sound.mp4 (video with audio)" -ForegroundColor White
Write-Host ""
Write-Host "Total time: $totalMinutes minutes, $totalSeconds seconds" -ForegroundColor Cyan
Write-Host ""
Write-Info "Video specifications:"
Write-Host "  • Resolution: 1920x1080 (Full HD)" -ForegroundColor White
Write-Host "  • Point density: ~5,000 points (lower)" -ForegroundColor White
Write-Host "  • Frame rate: 30 fps" -ForegroundColor White
Write-Host "  • Duration: 100 seconds (1:40)" -ForegroundColor White
Write-Host "  • Audio: AAC 192 kbps from H8InfiniteStars2.mp3" -ForegroundColor White
Write-Host "  • Effect: H8 (Heart Genesis with BPM-synchronized beats)" -ForegroundColor White
Write-Host ""
Write-Success "Ready to use! 🎥❤️"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow

exit 0


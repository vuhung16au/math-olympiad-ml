# Build Epic Heart Story (G2) at 2x Speed with Audio
# Generates the G2 effect at 60 fps (2x speed) and adds audio with fade-out
# Usage: .\scripts\build_g2_x2.ps1

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
Write-Section "Epic Heart Story (G2) - 2x Speed with Audio"
Write-Host ""
Write-Info "This script will generate the G2 epic heart animation at 2x speed (60 fps)"
Write-Info "and combine it with audio, resulting in a 68.5-second video."
Write-Host ""
Write-Info "Configuration:"
Write-Host "  Resolution: large (1920x1080)" -ForegroundColor White
Write-Host "  Density: lower (~5,000 points)" -ForegroundColor White
Write-Host "  Effect: G2 (Epic Heart Story)" -ForegroundColor White
Write-Host "  FPS: 60 (2x speed)" -ForegroundColor White
Write-Host "  Duration: 68.5 seconds" -ForegroundColor White
Write-Host "  Audio: Engima.mp3 with 2-second fade-out" -ForegroundColor White
Write-Host ""

# Estimate total time
$estimatedVideoTime = "15-25 minutes"
$estimatedAudioTime = "5-10 seconds"
Write-Info "Estimated time for video rendering: $estimatedVideoTime"
Write-Info "Estimated time for audio mixing: $estimatedAudioTime"
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
    Write-Host "  uv venv .venv" -ForegroundColor White
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  uv pip install -r requirements.txt" -ForegroundColor White
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
if (-not (Test-Path "Engima.mp3")) {
    Write-Error-Custom "✗ Engima.mp3 not found in current directory."
    Write-Info "Please ensure the audio file is present before running this script."
    exit 1
}
Write-Success "✓ Engima.mp3 found"

Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Proceed with generating the G2 animation and adding audio? (Y/n)"
if ($confirm -eq 'n' -or $confirm -eq 'N') {
    Write-Host "Build cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""

# Create outputs directory if it doesn't exist
if (-not (Test-Path "outputs")) {
    New-Item -ItemType Directory -Path "outputs" | Out-Null
    Write-Info "Created outputs directory"
}

# Track overall progress
$totalStartTime = Get-Date

# Step 1: Generate the video
Write-Section "Step 1: Generating G2 Animation at 60 fps"
Write-Host ""
Write-Info "Output: outputs/heart_epic_story_2x.mp4"
Write-Host ""

$videoStartTime = Get-Date

$videoCommand = "& `"$venvPython`" heart_animation.py --effect G2 --resolution large --density lower --fps 60 --output outputs/heart_epic_story_2x.mp4"

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
        if (Test-Path "outputs/heart_epic_story_2x.mp4") {
            $fileSize = (Get-Item "outputs/heart_epic_story_2x.mp4").Length / 1MB
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

# Step 2: Add audio with fade-out
Write-Section "Step 2: Adding Audio with Fade-out"
Write-Host ""
Write-Info "Combining video with Engima.mp3..."
Write-Info "Output: outputs/heart_epic_story_2x-sound.mp4"
Write-Host ""

$audioStartTime = Get-Date

$audioCommand = "ffmpeg -i outputs/heart_epic_story_2x.mp4 -i Engima.mp3 -t 68.5 -af `"afade=t=out:st=66.5:d=2`" -c:v copy -c:a aac -b:a 192k outputs/heart_epic_story_2x-sound.mp4"

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
        if (Test-Path "outputs/heart_epic_story_2x-sound.mp4") {
            $fileSize = (Get-Item "outputs/heart_epic_story_2x-sound.mp4").Length / 1MB
            Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
        }
    } else {
        throw "Audio mixing returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Error-Custom "✗ Audio mixing failed: $_"
    Write-Info "Video without audio is available at: outputs/heart_epic_story_2x.mp4"
    exit 1
}

# Calculate total time
$totalEndTime = Get-Date
$totalDuration = $totalEndTime - $totalStartTime
$totalMinutes = [math]::Floor($totalDuration.TotalMinutes)
$totalSeconds = [math]::Floor($totalDuration.Seconds)

# Display final summary
Write-Section "Build Summary"
Write-Host ""
Write-Success "✓ Epic Heart Story (G2) with audio completed successfully!"
Write-Host ""
Write-Host "Generated files:" -ForegroundColor Cyan
Write-Host "  1. outputs/heart_epic_story_2x.mp4 (video only)" -ForegroundColor White
Write-Host "  2. outputs/heart_epic_story_2x-sound.mp4 (video with audio)" -ForegroundColor White
Write-Host ""
Write-Host "Total time: $totalMinutes minutes, $totalSeconds seconds" -ForegroundColor Cyan
Write-Host ""
Write-Info "Video specifications:"
Write-Host "  • Resolution: 1920x1080 (large)" -ForegroundColor White
Write-Host "  • Point density: ~5,000 points (lower)" -ForegroundColor White
Write-Host "  • Frame rate: 60 fps (2x speed)" -ForegroundColor White
Write-Host "  • Duration: 68.5 seconds" -ForegroundColor White
Write-Host "  • Audio: AAC 192 kbps with 2-second fade-out" -ForegroundColor White
Write-Host ""
Write-Success "Ready to upload to YouTube or share! 🎥❤️"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow

exit 0

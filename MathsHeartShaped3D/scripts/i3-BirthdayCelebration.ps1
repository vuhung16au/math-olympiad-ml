# Build Script for I3 Effect: Birthday Celebration - 11, 16, 2025
# Multi-heart visualization with 11 hearts, then 16 hearts, and number display
# Automates the complete workflow: audio analysis -> video generation -> audio combination

param(
    [string]$AudioFile = "inputs/Happy Birthday Song.mp3",
    [string]$Resolution = "large",
    [string]$Density = "lower",
    [int]$FPS = 30,
    [int]$Bitrate = 5000,
    [switch]$Formulas = $false,
    [switch]$SkipAnalysis = $false
)

# Calculate bitrate based on resolution if not explicitly provided
if ($Bitrate -eq 5000) {
    switch ($Resolution) {
        "small" { $Bitrate = 2000 }
        "medium" { $Bitrate = 3000 }
        "large" { $Bitrate = 5000 }
        "4k" { $Bitrate = 20000 }
        default { $Bitrate = 5000 }
    }
}

# Color functions for output
function Write-Section {
    param([string]$Text)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Info {
    param([string]$Text)
    Write-Host "[INFO] $Text" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Text)
    Write-Host "[SUCCESS] $Text" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Text)
    Write-Host "[ERROR] $Text" -ForegroundColor Red
}

# Check if virtual environment exists
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error-Custom "Virtual environment not found. Please run setup first:"
    Write-Host "  .\scripts\setup-env.ps1" -ForegroundColor Yellow
    exit 1
}

# Use venv Python explicitly
$pythonCmd = $venvPython

# Check for FFmpeg
$ffmpegCheck = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpegCheck) {
    Write-Error-Custom "FFmpeg not found in PATH. Please install FFmpeg first."
    exit 1
}

# Determine audio features file name
$audioBaseName = [System.IO.Path]::GetFileNameWithoutExtension($AudioFile)
$featuresFile = "${audioBaseName}_features.json"

Write-Section "I3 Effect Builder: Birthday Celebration - 11, 16, 2025"
Write-Host "Audio File: $AudioFile" -ForegroundColor White
Write-Host "Resolution: $Resolution" -ForegroundColor White
Write-Host "Density: $Density" -ForegroundColor White
Write-Host "FPS: $FPS" -ForegroundColor White
Write-Host "Bitrate: $Bitrate kbps" -ForegroundColor White
Write-Host "Formulas: $Formulas" -ForegroundColor White
Write-Host "Duration: Will be determined from audio file" -ForegroundColor White
Write-Host ""
Write-Host "Effect Features:" -ForegroundColor Yellow
Write-Host "  • Phase 1 (0-50%): 11 hearts in formation" -ForegroundColor White
Write-Host "  • Phase 2 (50-100%): 16 hearts in formation" -ForegroundColor White
Write-Host "  • Number Display: 11, 16, 2025 (text overlay)" -ForegroundColor White
Write-Host "  • Birthday Theme: November 16 celebration" -ForegroundColor White
Write-Host "  • Camera Modes: Multi-heart frame, formation view, individual focus" -ForegroundColor White
Write-Host ""

# Step 1: Analyze Audio
if (-not $SkipAnalysis) {
    Write-Section "Step 1: Analyzing Audio File"
    
    if (-not (Test-Path $AudioFile)) {
        Write-Error-Custom "Audio file not found: $AudioFile"
        exit 1
    }
    
    Write-Info "Analyzing $AudioFile..."
    Write-Host "  This may take several minutes for a long audio file..." -ForegroundColor Yellow
    Write-Host ""
    
    $analysisStartTime = Get-Date
    
    try {
        & $pythonCmd analyze_audio.py $AudioFile -o $featuresFile
        
        if ($LASTEXITCODE -ne 0) {
            throw "Audio analysis failed with exit code $LASTEXITCODE"
        }
        
        if (-not (Test-Path $featuresFile)) {
            throw "Features file was not created: $featuresFile"
        }
        
        $analysisEndTime = Get-Date
        $analysisDuration = $analysisEndTime - $analysisStartTime
        $minutes = [math]::Floor($analysisDuration.TotalMinutes)
        $seconds = [math]::Floor($analysisDuration.TotalSeconds) % 60
        
        Write-Success "Audio analysis completed successfully!"
        Write-Host "  Analysis time: $minutes minutes, $seconds seconds" -ForegroundColor White
        Write-Host "  Features file: $featuresFile" -ForegroundColor White
    } catch {
        Write-Host ""
        Write-Error-Custom "Audio analysis failed: $_"
        exit 1
    }
} else {
    Write-Section "Step 1: Skipping Audio Analysis"
    Write-Info "Using existing features file: $featuresFile"
    
    if (-not (Test-Path $featuresFile)) {
        Write-Error-Custom "Features file not found: $featuresFile"
        Write-Host "  Run without -SkipAnalysis to generate it first" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""

# Step 2: Generate Video
Write-Section "Step 2: Generating Heart Animation with I3 Effect"

# Generate output filename based on audio filename and resolution
$audioFileName = [System.IO.Path]::GetFileNameWithoutExtension($AudioFile)
$outputVideo = "outputs/i3_${audioFileName}_${Resolution}_video.mp4"

Write-Info "Generating video with I3 effect..."
Write-Host "  Output: $outputVideo" -ForegroundColor White
Write-Host "  Effect: I3 (Birthday Celebration - 11, 16, 2025)" -ForegroundColor White
Write-Host "  Resolution: $Resolution" -ForegroundColor White
Write-Host "  Density: $Density" -ForegroundColor White
Write-Host "  FPS: $FPS" -ForegroundColor White
Write-Host "  Bitrate: $Bitrate kbps" -ForegroundColor White
Write-Host "  Duration: Will match audio file length" -ForegroundColor White
Write-Host "  Hearts: 11 hearts (0-50%), then 16 hearts (50-100%)" -ForegroundColor White
Write-Host "  Numbers: 11, 16, 2025 displayed at strategic moments" -ForegroundColor White
Write-Host ""
Write-Host "  This will take time depending on audio duration and resolution..." -ForegroundColor Yellow
Write-Host "  Note: 11-16 hearts require significantly more processing time" -ForegroundColor Yellow
Write-Host ""

$videoStartTime = Get-Date

# Build command with proper quoting for filenames with special characters
$videoArgs = @(
    "heart_animation.py",
    "--effect", "I3",
    "--audio-features", $featuresFile,
    "--resolution", $Resolution,
    "--density", $Density,
    "--fps", $FPS,
    "--bitrate", $Bitrate,
    "--output", $outputVideo
)

if ($Formulas) {
    $videoArgs += "--formulas"
}

try {
    & $pythonCmd $videoArgs
    
    if ($LASTEXITCODE -eq 0) {
        $videoEndTime = Get-Date
        $videoDuration = $videoEndTime - $videoStartTime
        $hours = [math]::Floor($videoDuration.TotalHours)
        $minutes = [math]::Floor($videoDuration.TotalMinutes) % 60
        $seconds = [math]::Floor($videoDuration.TotalSeconds) % 60
        
        Write-Host ""
        Write-Success "Video generation completed successfully!"
        Write-Host "  Render time: $hours hours, $minutes minutes, $seconds seconds" -ForegroundColor White
        
        # Get file size
        if (Test-Path $outputVideo) {
            $fileSize = (Get-Item $outputVideo).Length / 1MB
            Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
        }
    } else {
        throw "Video generation returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Error-Custom "Video generation failed: $_"
    exit 1
}

Write-Host ""

# Step 3: Combine Video with Audio
Write-Section "Step 3: Combining Video with Audio"

$finalOutput = "outputs/i3_${audioFileName}_${Resolution}_video+audio.mp4"

Write-Info "Combining $outputVideo with $AudioFile..."
Write-Host "  Output: $finalOutput" -ForegroundColor White
Write-Host "  Audio duration: Will match audio file length" -ForegroundColor White
Write-Host ""

$audioStartTime = Get-Date

# Get actual audio duration (use proper escaping for filename with apostrophes)
$audioDurationScript = @"
import librosa
import sys
y, sr = librosa.load(r'$AudioFile')
print(len(y) / sr)
"@
$audioDuration = & $pythonCmd -c $audioDurationScript

# Combine video with full audio (properly quote filenames)
$audioArgs = @(
    "-i", $outputVideo,
    "-i", $AudioFile,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    "-y",
    $finalOutput
)

try {
    & ffmpeg $audioArgs
    
    if ($LASTEXITCODE -eq 0) {
        $audioEndTime = Get-Date
        $audioDuration = $audioEndTime - $audioStartTime
        $seconds = [math]::Floor($audioDuration.TotalSeconds)
        
        Write-Host ""
        Write-Success "Audio combination completed successfully!"
        Write-Host "  Processing time: $seconds seconds" -ForegroundColor White
        
        # Get final file size
        if (Test-Path $finalOutput) {
            $finalSize = (Get-Item $finalOutput).Length / 1MB
            Write-Host "  Final file size: $([math]::Round($finalSize, 2)) MB" -ForegroundColor White
        }
    } else {
        throw "Audio combination returned non-zero exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Error-Custom "Audio combination failed: $_"
    Write-Host "  Video file is still available at: $outputVideo" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Final Summary
Write-Section "Build Complete!"

Write-Success "I3 Birthday Celebration animation is ready!"
Write-Host ""
Write-Host "Output Files:" -ForegroundColor Yellow
Write-Host "  • Video only: $outputVideo" -ForegroundColor White
Write-Host "  • Video + Audio: $finalOutput" -ForegroundColor White
Write-Host ""
Write-Host "Specifications:" -ForegroundColor Yellow
Write-Host "  • Resolution: $Resolution" -ForegroundColor White
Write-Host "  • Frame rate: $FPS fps" -ForegroundColor White
Write-Host "  • Duration: Matches audio file length" -ForegroundColor White
Write-Host "  • Audio: AAC 192 kbps from $AudioFile" -ForegroundColor White
Write-Host "  • Effect: I3 (Birthday Celebration - 11, 16, 2025)" -ForegroundColor White
Write-Host "  • Phase 1: 11 hearts (0-50% of duration)" -ForegroundColor White
Write-Host "  • Phase 2: 16 hearts (50-100% of duration)" -ForegroundColor White
Write-Host "  • Number Display: 11, 16, 2025 at strategic moments" -ForegroundColor White
Write-Host "  • Birthday Theme: November 16 celebration" -ForegroundColor White
Write-Host ""
Write-Success "Happy Birthday! 🎂🎉❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️🎵"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow

exit 0


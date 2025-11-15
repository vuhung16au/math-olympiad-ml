# Build Script for H8sync3min Effect (3.5 minute extended version)
# Automates the complete workflow: audio analysis -> video generation -> audio combination

param(
    [string]$AudioFile = "inputs/H8InfiniteStars2.mp3",
    [string]$Resolution = "large",
    [string]$Density = "lower",
    [int]$FPS = 30,
    [int]$Bitrate = 8000,
    [switch]$Formulas = $false,
    [switch]$SkipAnalysis = $false
)

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

Write-Section "H8sync3min Effect Builder - Extended 3.5 Minute Version"
Write-Host "Audio File: $AudioFile" -ForegroundColor White
Write-Host "Resolution: $Resolution" -ForegroundColor White
Write-Host "Density: $Density" -ForegroundColor White
Write-Host "FPS: $FPS" -ForegroundColor White
Write-Host "Bitrate: $Bitrate kbps" -ForegroundColor White
Write-Host "Formulas: $Formulas" -ForegroundColor White
Write-Host "Duration: 210 seconds (3:30)" -ForegroundColor White
Write-Host ""

# Step 1: Analyze Audio
if (-not $SkipAnalysis) {
    Write-Section "Step 1: Analyzing Audio File"
    
    if (-not (Test-Path $AudioFile)) {
        Write-Error-Custom "Audio file not found: $AudioFile"
        exit 1
    }
    
    Write-Info "Analyzing $AudioFile..."
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
Write-Section "Step 2: Generating Heart Animation with H8sync3min Effect"

$outputVideo = "outputs/h8sync3min_${Resolution}.mp4"

Write-Info "Generating video with H8sync3min effect..."
Write-Host "  Output: $outputVideo" -ForegroundColor White
Write-Host "  Effect: H8sync3min (Extended 3.5 minute Real Audio Sync)" -ForegroundColor White
Write-Host "  Resolution: $Resolution" -ForegroundColor White
Write-Host "  Density: $Density" -ForegroundColor White
Write-Host "  FPS: $FPS" -ForegroundColor White
Write-Host "  Bitrate: $Bitrate kbps" -ForegroundColor White
Write-Host "  Duration: 210 seconds (3:30)" -ForegroundColor White
Write-Host ""
Write-Host "  This will take approximately 15-30 minutes depending on your system..." -ForegroundColor Yellow
Write-Host ""

$videoStartTime = Get-Date

# Build command
$videoCommand = "& `"$pythonCmd`" heart_animation.py --effect H8sync3min --audio-features $featuresFile --resolution $Resolution --density $Density --fps $FPS --bitrate $Bitrate --output $outputVideo"

if ($Formulas) {
    $videoCommand += " --formulas"
}

try {
    Invoke-Expression $videoCommand
    
    if ($LASTEXITCODE -eq 0) {
        $videoEndTime = Get-Date
        $videoDuration = $videoEndTime - $videoStartTime
        $minutes = [math]::Floor($videoDuration.TotalMinutes)
        $seconds = [math]::Floor($videoDuration.TotalSeconds) % 60
        
        Write-Host ""
        Write-Success "Video generation completed successfully!"
        Write-Host "  Render time: $minutes minutes, $seconds seconds" -ForegroundColor White
        
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

$finalOutput = "outputs/h8sync3min_${Resolution}_with_audio.mp4"

Write-Info "Combining $outputVideo with $AudioFile..."
Write-Host "  Output: $finalOutput" -ForegroundColor White
Write-Host "  Audio duration: 210 seconds (3:30)" -ForegroundColor White
Write-Host ""

$audioStartTime = Get-Date

# Combine video with full audio (210 seconds)
$audioCommand = "ffmpeg -i $outputVideo -i $AudioFile -t 210 -c:v copy -c:a aac -b:a 192k -shortest -y $finalOutput"

try {
    Invoke-Expression $audioCommand
    
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

Write-Success "H8sync3min animation with audio synchronization is ready!"
Write-Host ""
Write-Host "Output Files:" -ForegroundColor Yellow
Write-Host "  • Video only: $outputVideo" -ForegroundColor White
Write-Host "  • Video + Audio: $finalOutput" -ForegroundColor White
Write-Host ""
Write-Host "Specifications:" -ForegroundColor Yellow
Write-Host "  • Resolution: $Resolution" -ForegroundColor White
Write-Host "  • Frame rate: $FPS fps" -ForegroundColor White
Write-Host "  • Duration: 210 seconds (3:30)" -ForegroundColor White
Write-Host "  • Audio: AAC 192 kbps from $AudioFile" -ForegroundColor White
Write-Host "  • Effect: H8sync3min (Extended Heart Genesis with Real Audio Sync)" -ForegroundColor White
Write-Host ""
Write-Success "Ready to use! 🎥❤️🎵"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow

exit 0


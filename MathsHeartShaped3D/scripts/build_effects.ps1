# Build Effects Test Script
# Generates heart animations with all 4 effect modes for comparison
# Usage: .\scripts\build_effects.ps1

# Configuration
$resolution = "small"
$density = "lower"
$effects = @("A", "B", "C", "D", "E", "F", "G")

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
Write-Section "3D Heart Animation - Effect Comparison Builder"
Write-Host ""
Write-Info "This script will generate 7 animations, one for each effect mode:"
Write-Host "  Effect A: Multi-axis rotation (Y + X wobble)" -ForegroundColor White
Write-Host "  Effect B: Dynamic camera orbit" -ForegroundColor White
Write-Host "  Effect C: Combined (rotation + camera + zoom)" -ForegroundColor White
Write-Host "  Effect D: Custom (Y rotation + elevation sweep + zoom)" -ForegroundColor White
Write-Host "  Effect E: Heartbeat Pulse (rhythmic scaling)" -ForegroundColor White
Write-Host "  Effect F: Spiral Ascent (spiral camera + zoom out)" -ForegroundColor White
Write-Host "  Effect G: Figure-8 Dance (infinity symbol camera path)" -ForegroundColor White
Write-Host ""
Write-Info "Configuration:"
Write-Host "  Resolution: $resolution (640x480)" -ForegroundColor White
Write-Host "  Density: $density (~5,000 points)" -ForegroundColor White
Write-Host "  Total videos: 7" -ForegroundColor White
Write-Host ""

# Estimate total time
$estimatedTimePerVideo = "2-5 minutes"
$estimatedTotalTime = "14-35 minutes"
Write-Info "Estimated time per video: $estimatedTimePerVideo"
Write-Info "Estimated total time: $estimatedTotalTime"
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

Write-Host ""

# Confirm before proceeding
$confirm = Read-Host "Proceed with generating all 7 effect animations? (Y/n)"
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
$successCount = 0
$failCount = 0
$results = @()

# Effect descriptions
$effectDescriptions = @{
    'A' = 'Multi-axis rotation'
    'B' = 'Dynamic camera orbit'
    'C' = 'Combined effects'
    'D' = 'Custom animation'
    'E' = 'Heartbeat Pulse'
    'F' = 'Spiral Ascent'
    'G' = 'Figure-8 Dance'
}

# Loop through each effect
for ($i = 0; $i -lt $effects.Count; $i++) {
    $effect = $effects[$i]
    $effectNum = $i + 1
    $effectName = $effectDescriptions[$effect]
    $outputPath = "outputs/heart_animation-effect$effect.mp4"
    
    Write-Section "Effect $effect ($effectNum of 7): $effectName"
    Write-Host ""
    Write-Info "Output: $outputPath"
    Write-Host ""
    
    # Record start time for this effect
    $startTime = Get-Date
    
    # Run the Python script
    $command = "& `"$venvPython`" heart_animation.py --resolution $resolution --density $density --effect $effect --output `"$outputPath`""
    
    try {
        Invoke-Expression $command
        
        if ($LASTEXITCODE -eq 0) {
            $endTime = Get-Date
            $duration = $endTime - $startTime
            $minutes = [math]::Floor($duration.TotalMinutes)
            $seconds = [math]::Floor($duration.Seconds)
            
            Write-Host ""
            Write-Success "✓ Effect $effect completed successfully!"
            Write-Host "  Render time: $minutes minutes, $seconds seconds" -ForegroundColor White
            
            # Get file size
            if (Test-Path $outputPath) {
                $fileSize = (Get-Item $outputPath).Length / 1MB
                Write-Host "  File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor White
            }
            
            $successCount++
            $results += [PSCustomObject]@{
                Effect = $effect
                Description = $effectName
                Status = "Success"
                Duration = "$minutes min, $seconds sec"
                Output = $outputPath
            }
        } else {
            throw "Python script returned non-zero exit code: $LASTEXITCODE"
        }
    } catch {
        Write-Host ""
        Write-Error-Custom "✗ Effect $effect failed: $_"
        $failCount++
        $results += [PSCustomObject]@{
            Effect = $effect
            Description = $effectName
            Status = "Failed"
            Duration = "N/A"
            Output = $outputPath
        }
    }
    
    Write-Host ""
    
    # Show progress
    $remaining = $effects.Count - $effectNum
    if ($remaining -gt 0) {
        Write-Info "Progress: $effectNum of $($effects.Count) completed. $remaining remaining..."
        Write-Host ""
    }
}

# Calculate total time
$totalEndTime = Get-Date
$totalDuration = $totalEndTime - $totalStartTime
$totalMinutes = [math]::Floor($totalDuration.TotalMinutes)
$totalSeconds = [math]::Floor($totalDuration.Seconds)

# Display final summary
Write-Section "Build Summary"
Write-Host ""

if ($successCount -eq $effects.Count) {
    Write-Success "✓ All $($effects.Count) animations generated successfully!"
} elseif ($successCount -gt 0) {
    Write-Host "Partial success: $successCount succeeded, $failCount failed" -ForegroundColor Yellow
} else {
    Write-Error-Custom "✗ All animations failed to generate."
}

Write-Host ""
Write-Host "Results:" -ForegroundColor Cyan
Write-Host ""

# Display results table
foreach ($result in $results) {
    $statusColor = if ($result.Status -eq "Success") { "Green" } else { "Red" }
    Write-Host "  Effect $($result.Effect) - $($result.Description)" -ForegroundColor White
    Write-Host "    Status: " -NoNewline
    Write-Host $result.Status -ForegroundColor $statusColor
    Write-Host "    Duration: $($result.Duration)" -ForegroundColor White
    Write-Host "    Output: $($result.Output)" -ForegroundColor White
    Write-Host ""
}

Write-Host "Total time: $totalMinutes minutes, $totalSeconds seconds" -ForegroundColor Cyan
Write-Host ""

if ($successCount -gt 0) {
    Write-Info "Generated videos are in the 'outputs' directory:"
    foreach ($result in $results | Where-Object { $_.Status -eq "Success" }) {
        Write-Host "  $($result.Output)" -ForegroundColor White
    }
    Write-Host ""
    Write-Info "Compare the effects to see the differences in animation styles!"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow

exit $(if ($successCount -eq $effects.Count) { 0 } else { 1 })

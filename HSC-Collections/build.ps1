# PowerShell build script for HSC-Collections.tex
# Usage: .\build.ps1 [pdf|clean|release]

param(
    [string]$Target = "pdf"
)

$TEXFILE = "HSC-Collections"
$PDFFILE = "$TEXFILE.pdf"
$RELEASE_DIR = "releases"
$CURRENT_DIR = (Get-Location).Path

function Build-PDF {
    Write-Host "Compiling LaTeX document..." -ForegroundColor Green
    
    # First pass
    $cmd = "docker run --rm -v `"${CURRENT_DIR}:/workdir`" -w /workdir texlive/texlive:latest pdflatex -interaction=nonstopmode $TEXFILE.tex"
    Invoke-Expression $cmd | Out-Null
    
    # Second pass (for cross-references)
    Invoke-Expression $cmd | Out-Null
    
    # Check if PDF was created (more reliable than exit codes)
    Start-Sleep -Milliseconds 500
    if (Test-Path $PDFFILE) {
        Write-Host "PDF compiled successfully: $PDFFILE" -ForegroundColor Green
    } else {
        Write-Host "PDF compilation failed - no PDF file was created!" -ForegroundColor Red
        exit 1
    }
}

function Clean-AuxFiles {
    Write-Host "Cleaning auxiliary files..." -ForegroundColor Yellow
    $auxFiles = @("aux", "log", "out", "toc", "pdf")
    foreach ($ext in $auxFiles) {
        $file = "$TEXFILE.$ext"
        if (Test-Path $file) {
            Remove-Item $file
            Write-Host "Removed $file" -ForegroundColor Gray
        }
    }
}

function Release-PDF {
    if (-not (Test-Path $PDFFILE)) {
        Write-Host "PDF not found. Building first..." -ForegroundColor Yellow
        Build-PDF
    }
    
    if (-not (Test-Path $RELEASE_DIR)) {
        New-Item -ItemType Directory -Path $RELEASE_DIR | Out-Null
    }
    
    Copy-Item $PDFFILE -Destination $RELEASE_DIR
    Write-Host "PDF copied to $RELEASE_DIR/$PDFFILE" -ForegroundColor Green
}

switch ($Target.ToLower()) {
    "pdf" { Build-PDF }
    "clean" { Clean-AuxFiles }
    "release" { Release-PDF }
    default {
        Write-Host "Unknown target: $Target" -ForegroundColor Red
        Write-Host "Usage: .\build.ps1 [pdf|clean|release]" -ForegroundColor Yellow
        exit 1
    }
}


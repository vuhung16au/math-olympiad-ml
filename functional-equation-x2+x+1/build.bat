@echo off
REM Windows batch script for building functional-equation-x2+x+1.tex
REM Usage: build.bat [pdf|clean|release]

set TEXFILE=functional-equation-x2+x+1
set PDFFILE=%TEXFILE%.pdf
set RELEASE_DIR=releases

if "%1"=="pdf" goto build
if "%1"=="clean" goto clean
if "%1"=="release" goto release
if "%1"=="" goto build

:build
echo Compiling LaTeX document...
REM Check if pdflatex is available locally
where pdflatex >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Using local pdflatex installation...
    pdflatex -interaction=nonstopmode %TEXFILE%.tex
    pdflatex -interaction=nonstopmode %TEXFILE%.tex
    if %ERRORLEVEL% EQU 0 (
        echo PDF compiled successfully: %PDFFILE%
    ) else (
        echo Compilation failed!
        exit /b 1
    )
) else (
    echo Using Docker for LaTeX compilation...
    docker run --rm -v "%CD%:/workdir" -w /workdir texlive/texlive:latest pdflatex -interaction=nonstopmode %TEXFILE%.tex 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Docker compilation failed! Please install LaTeX or ensure Docker is running.
        exit /b 1
    )
    docker run --rm -v "%CD%:/workdir" -w /workdir texlive/texlive:latest pdflatex -interaction=nonstopmode %TEXFILE%.tex 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo PDF compiled successfully: %PDFFILE%
    ) else (
        echo Compilation failed!
        exit /b 1
    )
)
goto end

:clean
echo Cleaning auxiliary files...
del /Q %TEXFILE%.aux %TEXFILE%.log %TEXFILE%.out %TEXFILE%.toc %TEXFILE%.pdf 2>nul
goto end

:release
if not exist %PDFFILE% (
    echo PDF not found. Building first...
    call :build
)
if not exist %RELEASE_DIR% mkdir %RELEASE_DIR%
copy %PDFFILE% %RELEASE_DIR%\
echo PDF copied to %RELEASE_DIR%\%PDFFILE%
goto end

:end

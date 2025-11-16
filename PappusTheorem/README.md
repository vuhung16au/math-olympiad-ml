# Pappus's Theorem

This repository contains a comprehensive mathematical treatment of Pappus's Theorem, one of the fundamental results in projective geometry. The document is designed for olympiad-level high school students and advanced mathematics enthusiasts.

## Problem Description

Pappus's Theorem states that if $A, B, C$ are three distinct points on a line $g$, and $a, b, c$ are three distinct points on another line $h$, then the three intersection points:
- $X = (Ab) \cap (aB)$
- $Y = (Ac) \cap (aC)$
- $Z = (Bc) \cap (bC)$

are collinear. This common line is called the **Pappus line**.

## Contents

The document covers:

1. **Overview**: Introduction to Pappus's Theorem and its significance
2. **Problem Statements**: 
   - General statement with TikZ diagrams
   - Special case: parallel lines
   - Special case: perpendicular lines
3. **History**: Brief history of Pappus of Alexandria and the theorem
4. **Required Knowledge**: Prerequisites including linear algebra, affine transformations, and projective geometry
5. **Solutions**: Two proof approaches:
   - Affine transformation method (computational)
   - Pascal's Theorem method (elegant and conceptual)
6. **Pascal's Theorem**: 
   - Statement and illustrations for ellipse, parabola, and hyperbola
   - High-level proof outline
   - Connection to Pappus's Theorem
7. **Future Works and Open Problems**: Research directions
8. **Conclusions**: Summary and insights

## Key Techniques

The solutions employ:

1. **Affine Transformations**: Simplifying geometric problems by transforming to convenient coordinate systems while preserving collinearity
2. **Projective Geometry**: Viewing two lines as a degenerate conic to connect Pappus's Theorem to Pascal's Theorem
3. **Coordinate Geometry**: Direct algebraic verification in simplified coordinate systems

## Compilation

### Prerequisites

- Docker (for LaTeX compilation)
- Make (optional, for using the Makefile)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode PappusTheorem.tex
```

Run the command twice to resolve all cross-references.

### Using Make (Linux/macOS/Git Bash)

The repository includes a `Makefile` with the following targets:

- `make all` or `make pdf`: Compile the LaTeX document to PDF
- `make clean`: Remove auxiliary files (`.aux`, `.log`, `.out`, `.toc`, `.pdf`)
- `make release`: Compile the PDF and copy it to the `releases/` directory

Example:
```bash
make pdf
```

### Using PowerShell Script (Windows)

For Windows users, use the PowerShell script:

```powershell
.\build.ps1 pdf      # Compile PDF
.\build.ps1 clean    # Clean auxiliary files
.\build.ps1 release # Build and copy to releases/
```

### Using Batch Script (Windows)

Alternatively, use the batch file:

```cmd
build.bat pdf      # Compile PDF
build.bat clean    # Clean auxiliary files
build.bat release  # Build and copy to releases/
```

## File Structure

- `PappusTheorem.tex`: Main LaTeX document containing problem statements and solutions
- `Makefile`: Build automation
- `build.ps1`: PowerShell build script
- `build.bat`: Windows batch build script
- `README.md`: This file
- `.gitignore`: Excludes LaTeX auxiliary files from version control
- `releases/`: Directory for compiled PDF releases

## Author

Vu Hung Nguyen  

- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/
- Github: https://github.com/vuhung16au/


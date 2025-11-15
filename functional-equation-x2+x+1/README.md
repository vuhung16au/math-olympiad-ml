# Functional Equation: f(f(x)) = x² + x + 1

This repository contains a mathematical analysis of the functional equation $f(f(x)) = x^2 + x + 1$ where $f: \mathbb{R} \to \mathbb{R}$.

## Problem Description

We analyze functions that satisfy:
$$f(f(x)) = x^2 + x + 1$$

The polynomial $x^2 + x + 1$ is the third cyclotomic polynomial, closely related to the primitive cube roots of unity. This document explores:

- Properties and constraints on such functions
- Systematic derivation of specific values like $f(0)$ and $f(1)$
- Connections to dynamical systems and complex analysis
- Generalizations to other polynomials and higher iterations
- Open questions about existence, uniqueness, and regularity

## Mathematical Highlights

- **Cyclotomic Connection**: The polynomial $x^2 + x + 1$ relates to cube roots of unity through $\omega^2 + \omega + 1 = 0$ where $\omega = e^{2\pi i/3}$
- **Positivity**: The polynomial is always positive for real $x$, with minimum value $\frac{3}{4}$ at $x = -\frac{1}{2}$
- **Iteration Structure**: Understanding $f \circ f$ requires analyzing orbits and fixed points in the context of discrete dynamical systems

## Compilation

### Prerequisites

**Option 1: Docker (Recommended)**
- Docker Desktop installed and running

**Option 2: Local LaTeX Installation**
- A LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- The `pdflatex` command available in your PATH

The build scripts will automatically detect and use a local LaTeX installation if available, falling back to Docker if not.

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode functional-equation-x2+x+1.tex
```

Run the command twice to resolve all cross-references.

### Using Local pdflatex

If you have LaTeX installed locally:

```bash
pdflatex -interaction=nonstopmode functional-equation-x2+x+1.tex
pdflatex -interaction=nonstopmode functional-equation-x2+x+1.tex
```

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
.\build.ps1 release  # Build and copy to releases/
```

### Using Batch Script (Windows)

Alternatively, use the batch file:

```cmd
build.bat pdf       # Compile PDF
build.bat clean     # Clean auxiliary files
build.bat release   # Build and copy to releases/
```

## File Structure

- `functional-equation-x2+x+1.tex`: Main LaTeX document containing the analysis
- `build.ps1`: PowerShell build script for Windows
- `build.bat`: Batch build script for Windows
- `Makefile`: Build automation for Linux/macOS/Git Bash
- `README.md`: This file
- `blogging.txt`: Blog post draft about the functional equation
- `.gitignore`: Excludes LaTeX auxiliary files from version control
- `releases/`: Directory containing compiled PDF releases

## Key Sections

1. **Overview**: Introduction to functional equations and the significance of $x^2 + x + 1$
2. **Problem Statement**: Formal statement and initial observations
3. **Derivation Steps**: Systematic solution approach with substitutions and algebraic manipulation
4. **Further Work**: Connections to dynamical systems, continuity, and complex extensions
5. **Generalizations**: Extensions to other polynomials and higher iterations
6. **Conclusion**: Summary and open questions

## Author

Vu Hung Nguyen

- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/
- Github: https://github.com/vuhung16au/

## License

This work is part of the math-olympiad-ml repository. See the main repository LICENSE for details.

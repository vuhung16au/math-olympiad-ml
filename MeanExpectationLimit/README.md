# Limits of Generalized Mean Expectations

This repository contains a mathematical analysis of the limits of expectations of generalized means (power means) over the unit hypercube $[0,1]^n$ as $n \to \infty$.

## Problem Description

We evaluate limits of the form:
\[
\lim_{n \to \infty} \int_{[0,1]^n} H_p(x_1, \ldots, x_n) \, dx_1 \cdots dx_n,
\]
where $H_p$ is the generalized mean (power mean) defined as:
\[
H_p(\mathbf{x}) = \left( \frac{1}{n} \sum_{i=1}^n x_i^p \right)^{1/p}, \quad p \neq 0.
\]

Special cases include:
- **Minimum Mean**: $p \to -\infty$ (limit is $0$)
- **Harmonic Mean**: $p = -1$ (limit is $0$)
- **Geometric Mean**: $p \to 0$ (limit is $1/e$)
- **Arithmetic Mean**: $p = 1$ (limit is $1/2$)
- **Root Mean Square**: $p = 2$ (limit is $1/\sqrt{3}$)
- **Cubic Mean**: $p = 3$ (limit is $1/\sqrt[3]{4}$)
- **Maximum Mean**: $p \to +\infty$ (limit is $1$)

## Key Techniques

The solutions employ:
1. **Fubini-Tonelli Theorem**: For factorizing integrals over independent variables
2. **Strong Law of Large Numbers (SLLN)**: For establishing almost sure convergence of sample means
3. **Dominated Convergence Theorem**: For interchanging limits and expectations

## Compilation

### Prerequisites

- Docker (for LaTeX compilation)
- Make (optional, for using the Makefile)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode MeanExpectationLimit.tex
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

- `MeanExpectationLimit.tex`: Main LaTeX document containing problem statements and solutions
- `Makefile`: Build automation
- `README.md`: This file
- `.gitignore`: Excludes LaTeX auxiliary files from version control

## Author

Vu Hung Nguyen  

- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/
- Github: https://github.com/vuhung16au/



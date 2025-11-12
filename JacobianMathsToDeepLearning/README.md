# From Gaussian Integral to Deep Learning: The Jacobian Matrix and Its Applications

This repository contains a comprehensive LaTeX document exploring the fundamental role of the Jacobian matrix in mathematics and its critical applications in deep learning.

## Overview

The document begins with the classical Gaussian integral problem, demonstrating how the Jacobian transformation enables elegant solutions to otherwise intractable integrals. It then traces the evolution of this concept from multivariable calculus to modern machine learning, showing how the Jacobian serves as the mathematical backbone of backpropagation, optimization algorithms, and neural network training.

## Contents

The document covers:

- **Problem 1**: The Gaussian integral (Euler-Poisson integral) and its solution
- **Solution using Jacobian transformation**: Converting from Cartesian to polar coordinates
- **Jacobian determinant in multivariable calculus**: Definition, explanation, and applications
- **Analogy to single-variable calculus**: Connecting multivariable concepts to familiar single-variable results
- **Linear transformations**: Special case where the Jacobian is constant
- **Best linear approximation**: Using the Jacobian for local approximations
- **Optimization**: Jacobian's role in gradient descent and optimization algorithms
- **Deep learning applications**: Backpropagation, neural networks, and analysis
- **Advanced optimizations**: Newton's method and Jacobian-Enhanced Neural Networks (JENN)
- **Sigmoid functions**: How the Jacobian applies to activation functions
- **Jacobian Descent (JD)**: Multi-objective optimization techniques
- **Further works and open problems**: Current research directions
- **Conclusions**: Summary and key takeaways

## Prerequisites

- Docker (for compiling the LaTeX document)
- A LaTeX distribution (handled via Docker)

## Building the Document

### Using Make (Linux/Mac/Git Bash)

```bash
make pdf        # Build the PDF
make clean      # Remove auxiliary files
make release    # Build and copy PDF to release/ directory as JacobianMathsToDeepLearning.pdf
make all        # Same as make pdf
```

### Using PowerShell (Windows)

```powershell
.\build.ps1 pdf      # Build the PDF
.\build.ps1 clean    # Remove auxiliary files
.\build.ps1 release  # Build and copy PDF to release/ directory as JacobianMathsToDeepLearning.pdf
```

### Using Batch Script (Windows)

```cmd
build.bat pdf      # Build the PDF
build.bat clean    # Remove auxiliary files
build.bat release  # Build and copy PDF to release/ directory as JacobianMathsToDeepLearning.pdf
```

### Manual Docker Build

If you prefer to build manually using Docker:

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode jacobian.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode jacobian.tex
```

Note: The document is compiled twice to resolve cross-references and citations.

### Alternative: Using MiKTeX Docker Image

You can also use the MiKTeX Docker image as shown in the example:

```bash
docker run -ti -v miktex:/var/lib/miktex -v "$(pwd):/miktex/work" \
    -e MIKTEX_UID=$(id -u) miktex/miktex:essential \
    pdflatex jacobian.tex
```

## File Structure

```
.
├── jacobian.tex      # Main LaTeX source file
├── Makefile          # Build configuration for make
├── build.bat         # Windows batch build script
├── build.ps1         # PowerShell build script
├── README.md         # This file
├── .gitignore        # Git ignore patterns for LaTeX files
└── release/          # Directory for compiled PDFs (created by make release)
```

## Contact

- **LinkedIn**: [https://www.linkedin.com/in/nguyenvuhung/](https://www.linkedin.com/in/nguyenvuhung/)
- **GitHub**: [https://github.com/vuhung16au/](https://github.com/vuhung16au/)
- **Repository**: [https://github.com/vuhung16au/math-olympiad-ml/tree/main/MeanExpectationLimit](https://github.com/vuhung16au/math-olympiad-ml/tree/main/MeanExpectationLimit)

## License

This work is provided for educational and research purposes.


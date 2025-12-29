# HSC Mathematics Extension 2: Complex Numbers Mastery

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-ComplexNumbers. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project curates complex numbers problems tailored to HSC Mathematics Extension 2 students. Every problem is solved with comprehensive explanations written so motivated high-school learners can follow each step.

## Licensing
Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

CC links: https://creativecommons.org/licenses/by/4.0/ and https://creativecommons.org/licenses/by/4.0/legalcode

Software/code remains MIT-licensed per the repository root LICENSE.

## Overview

The booklet `HSC-ComplexNumbers.tex` is organised in two parts:

- **Part 1**: Detailed walk-throughs (15 problems) with every conversion, application of De Moivre's theorem, and geometric interpretation spelled out. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise write-ups with hints and solution sketches (49 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` before a short solution sketch. Divided into basic (17), medium (15), and advanced (17) difficulty levels.

The collection contains **64 total problems** covering a comprehensive range of complex number techniques and applications.

## What This Collection Focuses On

- **Forms and Conversions**: Cartesian, polar, and exponential forms with modulus and argument
- **De Moivre's Theorem**: Powers and roots of complex numbers, trigonometric identities
- **Argand Diagram Geometry**: Sketching regions, loci, circles, lines, and geometric transformations
- **Polynomials**: Finding roots, factorization, properties of complex coefficients
- **Geometric Applications**: Vectors, distance, rotation, reflection, and scaling
- **Advanced Topics**: Euler's formula, complex proofs, and multi-step applications

All explanations prioritise plain, classroom-friendly language so Extension 2 students can see how to convert between forms, apply theorems safely, and justify geometric interpretations.

## Target Audience

- **HSC Math Extension 2 students** building confidence with complex number techniques.
- **Tutors** who need ready-to-use, step-by-step solutions plus quick-hint versions.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and emphasises communication of reasoning.

## Featured Problems

The collection includes classic and challenging complex number problems such as:

- **Basic Arithmetic**: Operations with complex numbers in various forms
- **Modulus-Argument Form**: Converting between representations and applying De Moivre
- **Loci and Regions**: Sketching complex inequalities on the Argand diagram
- **Polynomial Roots**: Finding complex roots and factorizing over the reals
- **Geometric Transformations**: Rotation, reflection, and vector applications
- **Trigonometric Identities**: Proving identities using Euler's formula
- **Advanced Proofs**: Complex geometric relationships and polynomial properties

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-ComplexNumbers.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-ComplexNumbers.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-ComplexNumbers.pdf`
- `make clean`: remove `.aux`, `.log`, `.toc`, and related artefacts
- `make release`: build the PDF and copy it to `releases/`
- `make open`: open the compiled PDF in your default viewer

Example:

```bash
make pdf
make open
```

Or build and open in one line:

```bash
make pdf && make open
```

## How to Use the Booklet

### For Students

1. Attempt each problem cold before checking any hints.
2. Only flip the upside-down hint (Part 2) if you need a nudge.
3. Compare your reasoning with the detailed Part 1 solution, paying attention to form conversions and theorem applications.
4. Re-work problems without notes to cement the technique.

### For Tutors

- Assign Part 1 problems as worked examples and Part 2 as coached practice.
- Use the hints to scaffold conversations without revealing complete solutions immediately.

### For Educators

- Embed individual problems into enrichment lessons or assessment preparation.
- Highlight the explicit application of theorems and geometric interpretations to reinforce good mathematical communication.

## Repository Layout

- `HSC-ComplexNumbers.tex`: Main LaTeX source with both parts and conclusion.
- `Makefile`: Docker-based build automation.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-ComplexNumbers.pdf`.
- `samples/`: Reference problems and source material from HSC past papers and resources.
- `problems/`: Part-wise problem+solution snippets organized by difficulty that are `\input` into the main TeX file:
  - `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex` (5 problems each)
  - `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex` (17, 15, and 17 problems respectively)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (colors, hint box, problem environments):
  - `dl101-colors.sty`: Color definitions for consistent formatting
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem and solution environment definitions
- `releases/`: Compiled PDFs (empty until you run `make release`).

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-ComplexNumbers


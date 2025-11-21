# HSC Mathematics Extension 2: Induction Mastery

This project curates mathematical induction problems tailored to HSC Mathematics Extension 2 students. Every problem is solved with induction and written so motivated high-school learners can follow each step.

## Overview

The booklet `HSC-Induction.tex` is organised in two parts:

- **Part 1**: Detailed walk-throughs (15 problems) with every base case, hypothesis, and inductive step spelled out. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise write-ups with hints and solution sketches (31 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` before a short solution sketch. Divided into basic (7), medium (10), and advanced (14) difficulty levels.

The collection contains **46 total problems** covering a comprehensive range of induction techniques and applications.

## What This Collection Focuses On

- **Summation formulas**: Arithmetic, geometric, and weighted series
- **Inequalities**: Power comparisons, factorial bounds, Bernoulli's inequality
- **Divisibility**: Modular arithmetic and number theory applications
- **Complex numbers**: De Moivre's formula and trigonometric identities
- **Trigonometry**: Summation of sines/cosines, arctangent identities, cosecant formulas
- **Recurrence relations**: Fibonacci-like sequences, nested radicals, characteristic equations
- **Calculus**: Integration by parts with inductive formulas
- **Combinatorics**: Binomial theorem, Pascal's identity, tiling problems
- **Number theory**: Wilson's theorem, Fermat's Little Theorem

All explanations prioritise plain, classroom-friendly language so Extension 2 students can see how to set up hypotheses, manipulate algebra safely, and justify each transition.

## Target Audience

- **HSC Math Extension 2 students** building confidence with induction-based arguments.
- **Tutors** who need ready-to-use, step-by-step solutions plus quick-hint versions.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and emphasises communication of reasoning.

## Featured Problems

The collection includes classic and challenging induction problems such as:

- **Nested Radicals**: Proving $\sqrt{2+\sqrt{2+\sqrt{2+\cdots}}} = 2\cos\frac{\pi}{2^{n+1}}$
- **Arctangent Sums**: Showing $\sum_{j=1}^{n}\tan^{-1}\left(\frac{1}{2j^2}\right) = \tan^{-1}\left(\frac{n}{n+1}\right)$
- **Recursive Sequences**: Proving formulas involving $(1+\sqrt{2})^n + (1-\sqrt{2})^n$
- **Trigonometric Identities**: Sum formulas for $\cos\theta + \cos 3\theta + \cdots + \cos(2n-1)\theta$
- **Factorial Inequalities**: $(2n)! \ge 2^n (n!)^2$ and $\sqrt{n!} > 2^n$ for large $n$
- **Advanced Theorems**: Binomial Theorem, Wilson's Theorem, Fermat's Little Theorem
- **Geometric Puzzles**: Tower of Hanoi, defective chessboard tiling
- **Calculus Integration**: Proving closed forms for $\int_0^x t^n e^{-t} dt$ and related integrals

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Induction.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Induction.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Induction.pdf`
- `make clean`: remove `.aux`, `.log`, `.toc`, and related artefacts
- `make release`: build the PDF and copy it to `releases/`

Example:

```bash
make pdf
```

## How to Use the Booklet

### For Students

1. Attempt each problem cold before checking any hints.
2. Only flip the upside-down hint (Part 2) if you need a nudge.
3. Compare your reasoning with the detailed Part 1 solution, paying attention to how the hypothesis is invoked.
4. Re-work problems without notes to cement the technique.

### For Tutors

- Assign Part 1 problems as worked examples and Part 2 as coached practice.
- Use the hints to scaffold conversations without revealing complete solutions immediately.

### For Educators

- Embed individual problems into enrichment lessons or assessment preparation.
- Highlight the explicit statement of hypotheses to reinforce good proof communication.

## Repository Layout

- `HSC-Induction.tex`: Main LaTeX source with both parts and conclusion.
- `Makefile`: Docker-based build automation.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-Induction.pdf`.
- `samples/`: Reference problems and source material from HSC past papers and resources.
- `problems/`: Part-wise problem+solution snippets organized by difficulty that are `\input` into the main TeX file:
  - `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex` (5 problems each)
  - `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex` (7, 10, and 14 problems respectively)
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
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Induction


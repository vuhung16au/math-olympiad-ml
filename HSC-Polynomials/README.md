# HSC Mathematics Extension 2: Polynomials Mastery

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Polynomials. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project curates polynomial problems tailored to HSC Mathematics Extension 2 students. Every problem covers essential polynomial techniques including complex numbers, roots of unity, Vieta's formulas, De Moivre's theorem, and transformations of roots, written so motivated high-school learners can follow each step.

## Overview

The booklet `HSC-Polynomials.tex` is organised in two parts:

- **Part 1**: Detailed walk-throughs (15 problems) with comprehensive strategy explanations, step-by-step solutions, and key takeaways. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise write-ups with upside-down hints and solution sketches (23 problems). Each problem includes a rotated hint before a concise solution. Divided into basic (5), medium (13), and advanced (5) difficulty levels.

The collection contains **38 total problems** covering a comprehensive range of polynomial techniques and applications.

## What This Collection Focuses On

- **Factoring Polynomials**: Factor theorem, synthetic division, finding all factors
- **Roots of Polynomials**: Finding roots, conjugate root theorem, relationship between roots and coefficients
- **Vieta's Formulas (Advanced)**: Sum and product relationships, constructing polynomials from root conditions—an essential beyond-syllabus technique
- **Complex Numbers**: Solving polynomials with complex coefficients, Cartesian and polar forms, complex roots in conjugate pairs
- **Transformations of Roots**: Forming polynomials with reciprocal, squared, shifted, or scaled roots
- **Nature of Roots**: Multiple (repeated) roots using derivatives, discriminant conditions, P(α)=0 and P'(α)=0 criterion
- **De Moivre's Theorem**: Roots of unity, expressing trigonometric functions as polynomials, nth roots in polar form
- **Polynomials and Trigonometry**: Solving polynomial equations derived from trigonometric identities, tan nθ formulas

All explanations prioritise plain, classroom-friendly language so Extension 2 students can see how to apply conjugate root theorem, leverage Vieta's formulas, use calculus to determine nature of roots, and connect De Moivre's theorem to polynomial factorizations.

## Target Audience

- **HSC Math Extension 2 students** building advanced problem-solving skills with polynomials, complex numbers, and trigonometry.
- **Tutors** who need ready-to-use, comprehensive solutions plus quick-hint versions for guided practice.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and emphasises rigorous algebraic reasoning.

## Featured Problems

The collection includes classic and challenging polynomial problems such as:

- **Complex Roots**: Finding square roots of -i, solving quadratics with complex coefficients
- **Roots of Unity**: Working with 7th, 5th, and nth roots of unity, geometric and algebraic properties
- **Conjugate Root Theorem**: Using conjugate pairs to factor cubics and quartics with real coefficients
- **Vieta's Formulas**: Constructing polynomials from root conditions, finding sums and products of root combinations
- **De Moivre's Theorem**: Expressing tan 5θ in terms of tan θ, deriving trigonometric identities from complex exponentials
- **Transformations of Roots**: Forming new polynomials with reciprocal, squared, or shifted roots
- **Multiple Roots**: Using derivatives to identify double roots and determine polynomial structure
- **Advanced Applications**: Weighted sums of roots of unity, complex triangle inequalities, trigonometric product identities

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Polynomials.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Polynomials.tex
```

Run the container twice to resolve cross references and table of contents.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Polynomials.pdf`
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

1. Review the **Fundamentals Review** section to refresh key theorems: Conjugate Root Theorem, Factor Theorem, Vieta's Formulas, De Moivre's Theorem, and Nature of Roots.
2. Attempt each Part 1 problem without looking at solutions, focusing on identifying which techniques apply.
3. Compare your work against detailed solutions, paying attention to strategy paragraphs and technique justifications.
4. For Part 2, try problems first, then flip the page to read upside-down hints if needed.
5. Re-work challenging problems to cement understanding of Vieta's formulas, complex number manipulations, and De Moivre applications.

### For Tutors

- Assign Part 1 problems as worked examples to demonstrate comprehensive solution strategies.
- Use Part 2 problems for guided practice, revealing hints progressively as scaffolding.
- Emphasize Vieta's formulas and De Moivre's theorem as powerful advanced techniques that frequently appear in Extension 2 exams.

### For Educators

- Embed individual problems into enrichment lessons or examination preparation.
- Highlight the expanded treatment of Vieta's Formulas (beyond syllabus) and De Moivre's Theorem to prepare students for advanced polynomial questions.
- Use the fundamentals section as a comprehensive reference for polynomial theory.

## Repository Layout

- `HSC-Polynomials.tex`: Main LaTeX source with both parts, fundamentals review, and conclusion.
- `Makefile`: Docker-based build automation for compiling the PDF.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-Polynomials.pdf`.
- `PLAN.md`: Comprehensive implementation plan documenting project structure and decisions.
- `PROBLEM_CLASSIFICATION.md`: Detailed classification of all 38 problems by difficulty, topics, and techniques.
- `SELECTION_SUMMARY.md`: Problem selection rationale and distribution across Part 1 and Part 2.
- `samples/`: Reference problems (01.tex through 38.tex, plus 00-basic.tex) from HSC past papers and resources.
- `problems/`: Part-wise problem+solution files organized by difficulty, `\input` into the main TeX file:
  - `fundamentals.tex`: Comprehensive review of polynomial theory with expanded Vieta's Formulas and De Moivre's Theorem coverage
  - `part1-easy.tex`, `part1-medium.tex`, `part1-hard.tex` (5 problems each)
  - `part2-easy-hints.tex`, `part2-medium-hints.tex`, `part2-hard-hints.tex` (5, 13, and 5 problems respectively)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (colors, hint box, problem environments):
  - `dl101-colors.sty`: Color definitions for consistent formatting
  - `dl101-hints.sty`: Upside-down hint environment using `\rotatebox` for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem and solution environment definitions
- `releases/`: Compiled PDFs (empty until you run `make release`).

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/vuhung16au/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Polynomials

For questions, corrections, or suggestions, please open an issue on the GitHub repository.

## Licensing
This folder’s educational content (LaTeX sources, PDFs, problems, solutions, images, styles) is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). You may share and adapt with attribution. See [LICENSE.md](LICENSE.md) for details and attribution requirements. The project’s code, build scripts, and Makefiles remain under the MIT License per the repository root.

- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
- Folder license: [LICENSE.md](LICENSE.md)
- Preferred citation: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Polynomials. Available at https://github.com/vuhung16au/math-olympiad-ml/"

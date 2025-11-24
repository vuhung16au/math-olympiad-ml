# HSC Mathematics Extension 2: Integration Mastery

This project curates integration problems tailored to HSC Mathematics Extension 2 students. Every problem demonstrates essential integration techniques with solutions written so motivated high-school learners can follow each step.

## Overview

The booklet `HSC-Integrals.tex` is organised in two parts:

- **Part 1**: Detailed walk-throughs (15 problems) with strategy paragraphs, complete step-by-step solutions, takeaways boxes, and alternative approaches where relevant. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise write-ups with hints and solution sketches (~45 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` before a short solution sketch. Divided into basic (~15), medium (~15), and advanced (~15) difficulty levels.

The collection contains **~60 total problems** covering a comprehensive range of integration techniques and applications.

## What This Collection Focuses On

- **Basic Techniques**: Reverse chain rule, standard integrals, u-substitution
- **Advanced Substitution**: Trigonometric substitutions ($\sqrt{a^2-x^2}$, $\sqrt{a^2+x^2}$, $\sqrt{x^2-a^2}$), t-formula
- **Integration by Parts**: LIATE rule, single and multiple applications, cyclic integrals
- **Partial Fractions**: Linear factors, quadratic factors, repeated factors
- **Reduction Formulae**: Deriving recurrence relations using integration by parts, proving with induction
- **Volumes of Solids**: Disk method, washer method, cylindrical shells, general slicing with TikZ diagrams
- **Definite Integral Properties**: Symmetry (odd/even functions), King's property, integral inequalities
- **Special Techniques**: Rationalizing substitutions, definite integral manipulations

All explanations prioritise plain, classroom-friendly language so Extension 2 students can see how to choose techniques, execute calculations safely, and justify each transition.

## Target Audience

- **HSC Math Extension 2 students** building mastery with integration techniques and applications.
- **Tutors** who need ready-to-use, step-by-step solutions plus quick-hint versions for guided practice.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and emphasises systematic problem-solving.

## Featured Problem Topics

The collection includes classic and challenging integration problems such as:

- **Partial Fractions**: Decomposing rational functions with linear and quadratic factors
- **Trigonometric Substitutions**: Evaluating $\int x^3\sqrt{x^2-9}\,dx$ using $x = 3\sec\theta$
- **Reduction Formulae**: Proving $J_n = \frac{n-1}{n}J_{n-2}$ for $\int_0^{\pi/2}\sin^n\theta\,d\theta$
- **Volumes by Shells**: Finding volumes of revolution using cylindrical shell method
- **Multi-Part Problems**: Combining substitution, reduction formulae, and definite integral properties
- **Definite Integral Properties**: Using symmetry and King's property to simplify integrals
- **Integration by Parts**: Multiple applications including reduction to recurrence relations

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Integrals.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Integrals.tex
```

Run the container twice to resolve cross references and table of contents.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Integrals.pdf`
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

1. Review the fundamentals section to refresh integration techniques.
2. Attempt each problem without looking at solutions first.
3. For Part 2, only check the upside-down hint if you need a nudge.
4. Compare your reasoning with the detailed Part 1 solutions, paying attention to technique selection and justification.
5. Re-work problems without notes to cement understanding and build speed.

### For Tutors

- Assign Part 1 problems as worked examples and Part 2 as coached practice.
- Use the hints to scaffold conversations without revealing complete solutions immediately.
- Reference the appendices for quick formula lookups and technique decision-making guides.

### For Educators

- Embed individual problems into enrichment lessons or assessment preparation.
- Highlight the explicit strategy paragraphs to reinforce good problem-solving communication.
- Use the problem index (Appendix B) to quickly find examples of specific techniques.

## Repository Layout

- `HSC-Integrals.tex`: Main LaTeX source with both parts, fundamentals review, and appendices.
- `Makefile`: Docker-based build automation.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-Integrals.pdf`.
- `PLAN.md`: Comprehensive implementation plan for project development.
- `samples/`: Reference problems and source material including:
  - `00-basic.tex`: Comprehensive fundamentals review
  - `01.tex` - `64.tex`: Sample problems from various sources
- `problems/`: Part-wise problem+solution snippets organized by difficulty that are `\input` into the main TeX file:
  - `part1-easy.tex`, `part1-medium.tex`, `part1-hard.tex` (5 problems each)
  - `part2-easy.tex`, `part2-medium.tex`, `part2-hard.tex` (~15 problems each)
  - `appendix-a-formulas.tex`: Formula sheet
  - `appendix-b-index.tex`: Problem index by technique
  - `appendix-c-substitutions.tex`: Common substitutions guide
  - `appendix-d-flowchart.tex`: Integration by parts decision tree
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (colors, hint box, problem environments):
  - `dl101-colors.sty`: Color definitions for consistent formatting
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem, solution, and takeaways environment definitions
- `releases/`: Compiled PDFs (empty until you run `make release`).

## Appendices

The booklet includes four comprehensive appendices:

- **Appendix A: Formula Sheet** - Quick reference for standard integrals, integration techniques, and key formulas
- **Appendix B: Index by Technique** - Organized listing of all problems by primary integration method
- **Appendix C: Common Substitutions Guide** - When and how to use various substitution techniques
- **Appendix D: Integration by Parts Flowchart** - Visual decision tree for applying integration by parts

## Solution Format

### Part 1 (Detailed Solutions)
Each problem includes:
- **Boxed problem statement** for clarity
- **Strategy paragraph** explaining technique selection and rationale
- **Complete step-by-step solution** with annotations and justifications
- **Takeaways box** highlighting key insights and lessons
- **Alternative approaches** when relevant
- **TikZ diagrams** for volume problems and geometric interpretations

### Part 2 (Hints and Sketches)
Each problem includes:
- **Boxed problem statement**
- **Upside-down hint** suggesting the approach or technique
- **Concise solution sketch** with key steps
- **Brief takeaways box** with essential insights
- **Boxed final answer**

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Integrals

## License

This project follows the same license as the parent repository.

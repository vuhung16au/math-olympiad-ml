# HSC Mathematics Extension 2: Last Resorts Mastery

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-LastResorts. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project curates the most challenging problems from HSC Mathematics Extension 2 examinations---the notorious Problem 16, known as "Last Resorts." Every problem represents the pinnacle of high school mathematics, combining multiple advanced topics and requiring sophisticated problem-solving techniques.

## Overview

The booklet `HSC-LastResorts.tex` is organized in two parts:

- **Part 1**: Detailed solutions (15 problems) with comprehensive explanations, strategy discussions, and step-by-step reasoning. Divided into medium (5) and advanced (5) difficulty levels, plus 5 additional hard problems.
- **Part 2**: Concise solutions with upside-down hints (43 problems). Each problem includes a hint rendered via `styles/dl101-hints` before a solution sketch. Divided into easy (2), medium (20), and advanced (21) difficulty levels.

The collection contains **58 total problems** covering the full spectrum of Problem 16 topics and techniques.

## What This Collection Focuses On

- **Complex Numbers**: Geometric applications, polynomial analysis, roots of unity, argument/modulus regions
- **Vector Algebra & 3D Geometry**: Optimization on surfaces, cross products, projections, distance problems
- **Advanced Inequalities**: AM-GM applications, Cauchy-Schwarz techniques, optimization constraints
- **Calculus & Analysis**: Integration techniques, function analysis, curvature, infinite series
- **Polynomial Theory**: Newton's sums, root bounds, symmetric functions
- **Optimization**: Constraint problems, Lagrange multiplier concepts, geometric extrema
- **Proof Techniques**: Mathematical induction, contradiction, sophisticated multi-step arguments

All explanations prioritize mathematical maturity and rigorous reasoning, preparing Extension 2 students for the highest level of HSC mathematics.

## Target Audience

- **HSC Math Extension 2 students** aiming to master Problem 16 and achieve top results
- **Advanced learners** seeking to develop sophisticated problem-solving skills
- **Tutors** who need comprehensive solutions and progressive difficulty levels
- **Teachers** wanting resources that challenge their most capable students

## Featured Problems

The collection includes authentic and challenging Problem 16 scenarios such as:

- **Vector Optimization**: Ellipsoid constraints using Cauchy-Schwarz techniques
- **Complex Analysis**: Root bounds using triangle inequality and geometric series
- **3D Geometry**: Skew line distances and sphere-plane optimization
- **Advanced Inequalities**: AM-GM applications in geometric optimization
- **Polynomial Theory**: Newton's sums and recurrence relation analysis
- **Calculus Applications**: Curvature analysis and osculating circles
- **Function Analysis**: Exponential vs polynomial comparisons
- **Mathematical Induction**: Advanced proof techniques and series bounds
- **Integration Techniques**: Wallis integrals and factorial bounds
- **Complex Geometry**: Rotation problems and equilateral triangle constructions

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-LastResorts.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-LastResorts.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-LastResorts.pdf`
- `make clean`: remove `.aux`, `.log`, `.toc`, and related artifacts
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

1. Study the fundamentals review section to refresh key theorems and techniques.
2. Attempt each problem independently before checking any solutions.
3. For Part 1: Compare your reasoning with detailed solutions, focusing on strategy and communication.
4. For Part 2: Use upside-down hints sparingly, then review concise solutions.
5. Rework problems from memory to cement understanding and build confidence.

### For Tutors

- Use Part 1 problems as worked examples to demonstrate advanced techniques.
- Assign Part 2 problems for independent practice with scaffolded hint support.
- Focus on proof communication and mathematical maturity development.

### for Educators

- Integrate problems into advanced Extension 2 courses and examination preparation.
- Use the progressive difficulty structure to challenge students appropriately.
- Emphasize the multi-topic integration characteristic of Problem 16.

## Repository Layout

- `HSC-LastResorts.tex`: Main LaTeX source with comprehensive content and structure.
- `Makefile`: Docker-based build automation for consistent PDF generation.
- `README.md`: Project overview and usage instructions (this file).
- `.gitignore`: Filters LaTeX artifacts, preserves `releases/HSC-LastResorts.pdf`.
- `samples/`: All 60 reference problems (01.tex to 60.tex) from authentic HSC scenarios.
- `problems/`: Part-wise problem collections organized by difficulty:
  - `part1-medium.tex`, `part1-hard.tex` (5 problems each)  
  - `part2-easy-hints.tex`, `part2-medium-hints.tex`, `part2-hard-hints.tex`
- `solutions/`: Reserved for standalone solution files and working documents.
- `styles/`: Shared LaTeX style files for consistent formatting:
  - `dl101-colors.sty`: Color definitions for mathematical content
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem and solution environment definitions
  - `dl101-boxes.sty`: Special boxes and formatting for enhanced presentation
- `releases/`: Compiled PDFs (populated via `make release`).
- `PROBLEM_CLASSIFICATION.md`: Comprehensive analysis of all sample problems by difficulty and topic.
- `SELECTION_SUMMARY.md`: Documentation of problem selection process and rationale.

## Project Philosophy

This project recognizes that Problem 16 represents more than computational skill---it demands mathematical maturity, strategic thinking, and the ability to synthesize diverse topics under examination pressure. The collection aims to:

- **Build Confidence**: Through progressive difficulty and comprehensive explanations
- **Develop Strategy**: By showing multiple approaches and technique selection reasoning  
- **Enhance Communication**: Through model solutions that demonstrate clear mathematical writing
- **Foster Maturity**: By presenting problems that require sophisticated mathematical thinking

## Conclusion & Good Luck!

Mastering Problem 16 is the culmination of your HSC Mathematics Extension 2 journey. These "Last Resort" problems will challenge you to integrate everything you've learned and push the boundaries of your mathematical capabilities.

Success in Problem 16 comes from persistence, pattern recognition, and the confidence to tackle unfamiliar scenarios with familiar tools. Use this collection as comprehensive preparation for the highest level of HSC mathematics.

Best of luck with your studies and HSC examinations!

## Contact Information

**Author**: Vu Hung Nguyen  
**LinkedIn**: https://www.linkedin.com/in/nguyenvuhung/  
**GitHub**: https://github.com/vuhung16au/  
**Repository**: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-LastResorts
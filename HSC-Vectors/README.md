# HSC Mathematics Extension 2: Vectors Mastery

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Vectors. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project curates high-quality vector problems tailored to HSC Mathematics Extension 2 students. Every problem covers essential 3D vector concepts with solutions that demonstrate both algebraic rigor and geometric intuition.

## Overview

The booklet `HSC-Vectors.tex` is organised in two parts:

- **Part 1**: Detailed solutions (14 problems) with complete algebraic steps, geometric diagrams, and key takeaways. Each problem uses compact notation to fit on one A4 page while maintaining clarity. Divided into basic (5), medium (5), and advanced (4) difficulty levels.
- **Part 2**: Concise solutions with hints (45 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` followed by a brief solution sketch. Divided into basic (15), medium (15), and advanced (15) difficulty levels.

The collection contains **59 total problems** providing comprehensive coverage of all vector topics in the Extension 2 syllabus.

## What This Collection Focuses On

- **3D Vectors & Coordinates**: Component form, magnitude calculations, distance formula in 3D space
- **Dot Product Applications**: Perpendicularity, angles between vectors, scalar and vector projections
- **Line Equations**: Parametric form, Cartesian conversion, parallel and skew lines
- **Geometric Proofs**: Pure vector proofs for parallelograms, triangles, centroids, tetrahedrons
- **Projections**: Scalar projection, vector projection, applications to distance problems
- **Angles**: Finding angles between vectors, lines, and in geometric configurations
- **Line Intersections**: Testing for intersection, finding intersection points, skew line identification
- **Spheres & Planes**: Vector and Cartesian equations, tangency conditions, intersections
- **Distance Calculations**: Point to line, point to plane, point to axis, shortest distances
- **Cross Product** (optional advanced): Formula, applications to area and normal vectors, distance calculations

All explanations prioritise clarity and geometric understanding alongside algebraic manipulation, helping Extension 2 students develop both computational skills and spatial intuition.

## Target Audience

- **HSC Math Extension 2 students** building mastery of 3D vectors and geometric applications.
- **Tutors** who need ready-to-use, comprehensive solutions plus guided practice problems with hints.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and covers all vector topics systematically.

## Featured Problems

The collection includes diverse and challenging vector problems such as:

- **Geometric Proofs**: Proving parallelogram properties, centroid locations, bimedian equalities for tetrahedrons
- **Sphere-Line Intersections**: Finding intersection points and angles for lines passing through spheres
- **Projectile Motion**: Vector proofs of parabolic paths and range equations
- **Complex Numbers & Vectors**: Connecting centroids on unit circles to cube roots and geometric loci
- **Cross Product Applications**: Computing areas, finding normal vectors, calculating distances
- **Cauchy-Schwarz Inequality**: Vector proofs on unit spheres with triangle inequality bounds
- **Tangency Problems**: Determining when lines are tangent to spheres using distance formulas
- **Collinearity & Ratio Proofs**: Using position vectors to prove points lie on lines and find section ratios
- **Perpendicular Line Systems**: Finding parameters for lines that intersect perpendicularly
- **3D Optimization**: Minimizing distances in 3D space using projections and geometric reasoning

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Vectors.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Vectors.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Vectors.pdf`
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

1. Read the Vectors Primer in the Introduction to review fundamental concepts and notation.
2. Attempt Part 1 problems independently, focusing on both algebraic manipulation and geometric interpretation.
3. Study the detailed solutions carefully, noting the compact notation techniques and geometric insights.
4. For Part 2 problems, make a genuine attempt before checking the upside-down hint.
5. Use the solution sketches to verify your approach, then fill in the detailed steps yourself.
6. Revisit challenging problems after a few days to reinforce techniques and build long-term understanding.

### For Tutors

- Use Part 1 problems as worked examples, highlighting both method and geometric meaning.
- Assign Part 2 problems for coached practice, using hints to guide without revealing solutions.
- Emphasize the connection between algebraic and geometric representations.
- Focus on helping students develop spatial visualization alongside computational skills.

### For Educators

- Embed problems into lesson sequences covering different vector topics.
- Use the comprehensive primer as a reference or revision resource.
- Highlight the cross product section for advanced students or extension activities.
- Assign problem sets targeting specific topics (projections, geometric proofs, sphere intersections, etc.).

## Repository Layout

- `HSC-Vectors.tex`: Main LaTeX source with comprehensive primer, both parts, and conclusion.
- `Makefile`: Docker-based build automation.
- `README.md`: Project overview (this file).
- `PLAN.md`: Detailed implementation plan for the project.
- `PROBLEM_CLASSIFICATION.md`: Complete classification table of all 60 sample problems by topic and difficulty.
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-Vectors.pdf`.
- `samples/`: 60 reference problems (01.tex through 60.tex) plus 00-basic.tex vectors primer source.
- `problems/`: Part-wise problem+solution snippets organized by difficulty that are `\input` into the main TeX file:
  - `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex` (5, 5, and 4 problems respectively)
  - `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex` (15 problems each)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (colors, hint box, problem environments):
  - `dl101-colors.sty`: Color definitions for consistent formatting
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem and solution environment definitions with takeaways boxes
- `releases/`: Compiled PDFs (empty until you run `make release`).

## Compact Notation Macros

To ensure Part 1 solutions fit on one A4 page while maintaining readability, the document defines several compact notation macros:

- `\cvec{x}{y}{z}`: Compact column vector using psmallmatrix
- `\tvec{x}{y}{z}`: Component form notation $x\mathbf{i}+y\mathbf{j}+z\mathbf{k}$
- `\tfrac{}{}`: LaTeX's text-style fractions (smaller than displaystyle)
- `\vspace{-2mm}`: Tighter vertical spacing between elements

These macros help compress solutions without sacrificing clarity or completeness.

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Vectors

---

*Good luck with your vectors mastery and the HSC examination!*

## Licensing
This folder’s educational content (LaTeX sources, PDFs, problems, solutions, images, styles) is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). You may share and adapt with attribution. See [LICENSE.md](LICENSE.md) for details and attribution requirements. The project’s code, build scripts, and Makefiles remain under the MIT License per the repository root.

- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
- Folder license: [LICENSE.md](LICENSE.md)
- Preferred citation: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Vectors. Available at https://github.com/vuhung16au/math-olympiad-ml/"

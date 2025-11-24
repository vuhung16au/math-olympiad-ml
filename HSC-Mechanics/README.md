# HSC Mathematics Extension 2: Mechanics Mastery

This project presents a comprehensive collection of mechanics problems for HSC Mathematics Extension 2 students. Every problem demonstrates key mathematical techniques including integration methods, differential equations, Newton's laws applications, and limiting behavior analysis.

## Overview

The booklet `HSC-Mechanics.tex` is organized in two parts:

- **Part 1**: Detailed step-by-step solutions (15 problems) with every force diagram, integration technique, and algebraic manipulation fully explained. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise solutions with strategic hints (49 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` to guide approach without revealing the solution. Divided into basic (11), medium (21), and advanced (17) difficulty levels.

The collection contains **64 total problems** covering all essential HSC Extension 2 mechanics topics.

## What This Collection Focuses On

- **Simple Harmonic Motion (SHM)**: Center of motion, period, amplitude calculations, velocity-displacement relationships
- **Variable Force Problems**: Finding velocity given position using $a = \frac{d}{dx}(\frac{1}{2}v^2)$
- **Resisted Motion**: Linear ($kv$) and quadratic ($kv^2$) resistance models, horizontal and vertical motion
- **Terminal Velocity**: Limiting behavior as $t \to \infty$, understanding $a = 0$ condition
- **Projectile Motion**: With and without air resistance, trajectory analysis, parametric equations
- **Force Analysis**: Newton's Second Law, inclined planes, multiple force systems, free body diagrams
- **Circular Motion**: Angular velocity, centripetal acceleration, period and frequency relationships
- **Calculus Applications**: Separation of variables, partial fractions, exponential decay, logarithmic integration

All solutions emphasize clear force diagrams, explicit sign conventions, systematic application of Newton's laws, and careful attention to initial conditions.

## Target Audience

- **HSC Math Extension 2 students** preparing for challenging mechanics problems and developing advanced problem-solving skills
- **Students** wanting to master the calculus-based approach to force analysis and motion
- **Tutors** who need comprehensive worked examples and problems with adjustable scaffolding (via hints)
- **Teachers** seeking quality supplementary materials aligned with NSW Extension 2 syllabus mechanics topics

## Featured Problems

The collection includes classic and challenging mechanics problems such as:

- **Projectile Trajectories**: Proving conditions for two possible trajectories using discriminant analysis
- **Terminal Velocity**: Deriving limiting velocity for particles falling through resistant media
- **SHM Collision**: Two particles in SHM meeting at specific positions and times
- **Magnetic Repulsion**: Inverse cube law forces with complex integration
- **Resisted Motion**: Particles with combined linear and cubic resistance ($v + v^3$)
- **Bungee Jumping**: SHM with shifted center of motion modeling elastic cord behavior
- **Projectile with Resistance**: Vector form analysis of motion with air resistance proportional to velocity
- **Envelope of Trajectories**: Finding the boundary curve tangent to all projectile paths
- **Inverse Square Law**: Gravitational attraction problems requiring advanced calculus techniques
- **Hyperbolic Functions**: Problems involving $\sinh$ and $\cosh$ in velocity equations

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Mechanics.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Mechanics.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Mechanics.pdf`
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

1. **Review the Mechanics Primer** in the Introduction section to refresh fundamental concepts and formulas.
2. **Master the "Golden Rule"** table—choosing the correct form of acceleration is critical for success.
3. **Attempt Part 1 problems** without looking at solutions. Focus on drawing clear force diagrams and stating positive direction.
4. **Compare your solutions** with the detailed explanations, noting integration techniques and sign convention handling.
5. **Move to Part 2 problems** using hints only after genuine attempts. Turn the page to read upside-down hints.
6. **Practice regularly**—mechanics requires both conceptual understanding and technical fluency with calculus.
7. **Revisit challenging problems** after a few days to reinforce understanding and technique.

### For Tutors

- Use Part 1 problems as fully worked examples in lessons, highlighting key techniques like choosing the right acceleration form.
- Assign Part 2 problems for homework or practice, encouraging students to attempt problems before revealing hints.
- Focus on force diagram construction and sign conventions—these are common sources of errors.
- Select problems by topic (SHM, resisted motion, projectiles) to target specific syllabus areas.
- Use the variety of difficulty levels to differentiate instruction for different student abilities.

### For Educators

- Incorporate problems into lesson plans, assessment preparation, or enrichment activities.
- Emphasize systematic application of Newton's Second Law and clear communication of reasoning.
- Use problems with TikZ diagrams to reinforce the importance of visual representation in physics.
- Assign multi-part problems to develop sustained problem-solving stamina needed for HSC examinations.

## Repository Layout

- `HSC-Mechanics.tex`: Main LaTeX source with Introduction (including Mechanics Primer), Part 1, Part 2, and Conclusion.
- `Makefile`: Docker-based build automation with OS-specific PDF opening.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artifacts, keeps `releases/HSC-Mechanics.pdf`.
- `PLAN.md`: Comprehensive implementation plan with phases, tasks, and success criteria.
- `PROBLEM_CLASSIFICATION.md`: Detailed analysis of all 64 sample problems by difficulty, topic, techniques, and structure.
- `SELECTION_SUMMARY.md`: Strategic selection justification for Part 1 and Part 2 problems with topic coverage verification.
- `samples/`: Original problem files from HSC past papers and quality resources (64 problems):
  - `00-basic.tex`: Fundamental mechanics concepts reference material
  - `01.tex` through `64.tex`: Individual mechanics problems
- `problems/`: Organized problem files by part and difficulty that are `\input` into main TeX:
  - `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex` (5 problems each, detailed solutions, no hints)
  - `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex` (11, 21, and 17 problems respectively, with hints)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (copied from HSC-Induction):
  - `dl101-colors.sty`: Color palette (bookpurple, bookred, bookblack, softivory)
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem, solution, and takeaways box environments
- `images/`: Pre-existing diagram files for force diagrams and geometric illustrations.
- `releases/`: Compiled PDFs (run `make release` to populate).
- `TODO/`: Reference materials and YouTube video links for mechanics topics.

## Problem Distribution

### Part 1: Detailed Solutions (15 problems)

| Difficulty | Count | Topics Covered |
|------------|-------|----------------|
| Basic | 5 | Circular motion basics, variable acceleration, projectile trajectories, simple integration |
| Medium | 5 | Projectile with air resistance, quadratic resistance, particle systems, combined resistance |
| Advanced | 5 | Magnetic repulsion, complex SHM, inverse square law, advanced calculus techniques |

### Part 2: Hints + Solutions (49 problems)

| Difficulty | Count | Topics Covered |
|------------|-------|----------------|
| Basic | 11 | SHM fundamentals, basic projectiles, simple resisted motion, Newton's laws |
| Medium | 21 | Combined SHM, parametric projectiles, terminal velocity, multi-step integration |
| Advanced | 17 | Bungee SHM, hyperbolic functions, exotic forces, envelope of trajectories, complex proofs |

## Key Techniques Covered

- **Integration Methods**: Separation of variables, partial fractions, substitution, standard integrals for exponential and logarithmic forms
- **Differential Equations**: First-order ODEs, initial value problems, limiting behavior analysis
- **Force Analysis**: Free body diagrams, Newton's Second Law, sign conventions, vector decomposition
- **SHM Analysis**: Period and frequency calculations, amplitude determination, center of motion, velocity-displacement relationships
- **Terminal Velocity**: Equilibrium conditions, limiting processes, exponential approach to limits
- **Projectile Analysis**: Parametric equations, trajectory derivation, maximum range/height, time of flight

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Mechanics

---

Good luck with your HSC Mathematics Extension 2 studies and examinations!

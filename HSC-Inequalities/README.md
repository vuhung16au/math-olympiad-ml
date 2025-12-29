# HSC Mathematics Extension 2: Inequalities Mastery

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Inequalities. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project curates inequality problems tailored to HSC Mathematics Extension 2 students. Each problem explores fundamental inequality techniques including AM-GM, Cauchy-Schwarz, triangle inequality, integration-based inequalities, and inequalities via mathematical induction. Every solution demonstrates rigorous proof techniques suitable for Extension 2 examinations.

## Licensing
Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

CC links: https://creativecommons.org/licenses/by/4.0/ and https://creativecommons.org/licenses/by/4.0/legalcode

Software/code remains MIT-licensed per the repository root LICENSE.

## Overview

The booklet `HSC-Inequalities.tex` is organised in two parts:

- **Part 1**: Detailed walk-throughs (15 problems) with complete step-by-step solutions and comprehensive takeaways highlighting key techniques and strategic insights. Divided into basic (5), medium (5), and advanced (5) difficulty levels.
- **Part 2**: Concise write-ups with hints and solution sketches (30 problems). Each problem includes an upside-down hint rendered via `styles/dl101-hints` before a brief solution, followed by concise takeaways. Divided into basic (8), medium (10), and advanced (12) difficulty levels.

The collection contains **45 total problems** covering all major inequality techniques in the HSC Extension 2 syllabus.

## What This Collection Focuses On

### The Five Key Inequality Types

1. **AM-GM Inequality**: Arithmetic mean-geometric mean applications including weighted forms, constrained optimization, and cyclic symmetric expressions (21 problems, ~48%)
2. **Cauchy-Schwarz Inequality**: Vector and algebraic forms, applications with constraints and sum-of-squares techniques (5 problems, ~11%)
3. **Integration Inequalities**: Comparison theorems, bound estimation, and limit applications including the definition of $e$ (3 problems, ~7%)
4. **Triangle Inequality**: Real and complex number variants, polynomial root bounds, and modulus inequalities (4 problems, ~9%)
5. **Inequalities via Induction**: Including Bernoulli's inequality, exponential bounds, and factorial estimates (11 problems, ~25%)

### Problem Characteristics

- **Multi-part problems**: 50% of problems have multiple parts requiring "hence" or "deduce" steps
- **Equality conditions**: Emphasis on identifying when inequalities become equalities
- **Proof techniques**: Direct proofs, proof by contradiction, substitution methods, and inductive reasoning
- **Real-world applications**: Optimization problems, geometric constraints, and calculus bounds

All explanations prioritise clear, classroom-friendly language so Extension 2 students can understand when to apply each technique, how to set up algebraic manipulations, and how to communicate complete proofs.

## Target Audience

- **HSC Math Extension 2 students** building mastery of inequality techniques for examinations and competitions.
- **Tutors** who need ready-to-use, step-by-step solutions plus quick-hint versions for scaffolded learning.
- **Teachers** who want a companion booklet that aligns with the NSW syllabus and emphasises strategic problem-solving with inequalities.

## Featured Problems

The collection includes classic and challenging inequality problems such as:

- **AM-GM Applications**:
  - Proving $(x+y)(y+z)(z+x) \ge 8xyz$ for positive reals
  - Constrained optimization with $\frac{1}{a}+\frac{1}{b}+\frac{1}{c}=1$
  - Young's inequality: $a^n b^{1-n} \ge na + (1-n)b$

- **Cauchy-Schwarz Mastery**:
  - QM-GM inequality derivations
  - Maximum value problems with constraint $x^2+y^2+z^2=25$
  - Vector inequalities on sphere coordinates
  
- **Integration Bounds**:
  - Proving $x > \ln(x)$ and deducing $e^{n^2+n} > (n!)^2$
  - Squeeze theorem applications to prove $\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n = e$
  
- **Triangle Inequality**:
  - Complex modulus bounds and polynomial root estimates
  - Geometric inequalities for triangle sides
  
- **Induction Techniques**:
  - Bernoulli's inequality: $(1+x)^n \ge 1+nx$ for various contexts
  - Exponential vs polynomial growth: $2^n \ge n^2-2$
  - Factorial bounds and binomial coefficient estimates

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Inequalities.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Inequalities.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Inequalities.pdf`
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

1. Read the **Introduction** section carefully to understand the five key inequality types and fundamental theorems.
2. Study the **Worked Examples** to see how each technique is applied in simple contexts.
3. Attempt Part 1 problems without hints, focusing on identifying which inequality technique to use.
4. Study the **Takeaways** sections to understand the strategic decisions and key insights.
5. For Part 2, only flip the upside-down hint if you need guidance on which approach to take.
6. Re-work problems after a few days to reinforce pattern recognition and technique selection.

### For Tutors

- Use Part 1 problems as worked examples, emphasizing the decision-making process for technique selection.
- Assign Part 2 problems as coached practice with hints available as scaffolding.
- Focus on the Takeaways to help students understand when and why to apply specific techniques.

### For Educators

- Embed problems into enrichment lessons or examination preparation.
- Use the progression from basic to advanced to differentiate instruction.
- Highlight the explicit identification of techniques to reinforce mathematical communication skills.

## Repository Layout

- `HSC-Inequalities.tex`: Main LaTeX source with introduction, worked examples, both parts, and conclusion.
- `Makefile`: Docker-based build automation.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artefacts, keeps `releases/HSC-Inequalities.pdf`.
- `samples/`: 45 inequality problems sourced from HSC past papers, textbooks, and competition problems (00-basic.tex through 44.tex).
- `problems/`: Part-wise problem+solution+takeaways snippets organized by difficulty that are `\input` into the main TeX file:
  - `part1-basic.tex`, `part1-medium.tex`, `part1-advanced.tex` (5 problems each with detailed solutions and full takeaways)
  - `part2-basic.tex`, `part2-medium.tex`, `part2-advanced.tex` (8, 10, and 12 problems respectively with hints and brief takeaways)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (colors, hint box, problem environments):
  - `dl101-colors.sty`: Color definitions for consistent formatting
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem, solution, and takeaways environment definitions
  - `dl101-boxes.sty`: Custom box styling for visual clarity
- `releases/`: Compiled PDFs (empty until you run `make release`).
- `TODO/`: Reference materials including inequality guides and YouTube resources.

## Difficulty Progression

### Easy Problems (13 total: 5 in Part 1, 8 in Part 2)

Direct application of AM-GM, Cauchy-Schwarz, triangle inequality, or basic induction. Single-step reasoning with clear technique identification.

### Medium Problems (15 total: 5 in Part 1, 10 in Part 2)

Multi-step problems requiring combination of 2-3 techniques, algebraic manipulation, substitution methods, or constrained optimization.

### Hard Problems (17 total: 5 in Part 1, 12 in Part 2)

Advanced problems requiring creative approaches, multiple complex techniques, sophisticated substitutions, or integration of calculus with inequalities.

## Conclusion

Inequalities are a cornerstone of the HSC Mathematics Extension 2 course, testing both technical skill and strategic thinking. By working through these 45 carefully curated problems, you will develop:

- **Pattern recognition**: Identifying which technique applies to each problem type
- **Proof-writing clarity**: Communicating mathematical arguments with precision
- **Strategic problem-solving**: Making decisions about substitutions, algebraic manipulation, and technique selection
- **Examination confidence**: Handling inequality problems efficiently under time pressure

Remember: the key to mastering inequalities is not just memorizing theorems, but understanding when and how to apply them. Use the Takeaways sections to build this strategic insight.

Best of luck with your studies and HSC examinations!

## Author

Vu Hung Nguyen

- LinkedIn: <https://www.linkedin.com/in/nguyenvuhung/>
- GitHub: <https://github.com/vuhung16au/>
- Repository: <https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Inequalities>


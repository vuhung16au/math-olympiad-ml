# HSC Mathematics Extension 2: Mathematical Proofs

## Attribution
© 2025 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2025). math-olympiad-ml — HSC-Proofs. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This project presents a comprehensive collection of mathematical proof problems for HSC Mathematics Extension 2 students. Every problem demonstrates key proof techniques including direct proof, proof by contradiction, mathematical induction, and proof by cases across fundamental number theory and algebra topics.

## Overview

The booklet `HSC-Proofs.tex` is organized in two parts:

- **Part 1**: Detailed step-by-step solutions (15 problems) with every logical step, algebraic manipulation, and proof technique fully explained. Includes comprehensive Takeaways sections. Divided into Easy (5), Medium (5), and Hard (5) difficulty levels.
- **Part 2**: Problems with strategic hints and solution sketches (15 problems). Each problem includes a hint (using `styles/dl101-hints`) to guide approach, followed by a condensed solution sketch showing key steps without full exposition. Divided into Easy (5), Medium (5), and Hard (5) difficulty levels.

The collection contains **30 total problems** covering essential proof techniques for HSC Extension 2 mathematics.

## What This Collection Focuses On

- **Number Theory**: Divisibility proofs, modular arithmetic, parity arguments, Diophantine equations
- **Irrational Numbers**: Proving irrationality using contradiction, properties of surds and logarithms
- **Mathematical Induction**: Divisibility induction, summation formulas, inequality proofs, nested radicals
- **Biconditional Proofs**: If and only if statements, logical equivalence
- **Multi-Part Proofs**: Combining multiple techniques, building arguments across connected parts
- **Proof by Cases**: Exhaustive case analysis, handling different scenarios systematically
- **Modular Arithmetic**: Congruence classes, properties of remainders, quadratic residues

All solutions emphasize clear logical structure, explicit statement of assumptions, systematic application of proof techniques, and rigorous mathematical communication.

## Target Audience

- **HSC Math Extension 2 students** preparing for challenging proof problems and developing rigorous mathematical reasoning
- **Students** wanting to master fundamental proof techniques and mathematical communication
- **Tutors** who need comprehensive worked examples and problems with adjustable scaffolding (via hints)
- **Teachers** seeking quality supplementary materials aligned with proof requirements in Extension 2 mathematics

## Featured Problems

The collection includes classic and challenging proof problems such as:

- **Divisibility Proofs**: Consecutive integers, difference of squares, products of consecutive numbers
- **Irrationality Proofs**: √2, √3, √6, log₂3, combining multiple techniques
- **Modular Arithmetic**: Powers mod n, quadratic residues, Diophantine equations
- **Parity Arguments**: Sum of squares, product properties, existence proofs
- **Mathematical Induction**: Divisibility by 7, 8, 6, nested radicals, sum formulas
- **Biconditional Proofs**: Divisibility rules, characterization theorems
- **Proof by Cases**: Odd/even analysis, remainder classes, exhaustive arguments
- **Multi-Part Proofs**: Building complex arguments from simple lemmas

## How to Build the PDF

### Prerequisites

- Docker (preferred for a consistent TeX environment)
- Make (optional, but convenient on macOS/Linux)

### Using Docker Directly

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Proofs.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Proofs.tex
```

Run the container twice to resolve cross references.

### Using Make (macOS/Linux/Git Bash)

Available targets:

- `make pdf` (default): build `HSC-Proofs.pdf`
- `make clean`: remove `.aux`, `.log`, `.out`, and related artifacts
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

1. **Review the Proof Primer** in the Introduction section to understand fundamental number theory concepts and proof techniques.
2. **Master the four proof techniques**—knowing when to use direct proof, contradiction, induction, or cases is critical.
3. **Attempt Part 1 problems** without looking at solutions. Focus on clear logical structure and explicit assumptions.
4. **Compare your solutions** with the detailed explanations, noting proof strategies and algebraic techniques.
5. **Study the Takeaways sections** after each Part 1 solution to extract key techniques and patterns.
6. **Move to Part 2 problems** using hints only after genuine attempts. Turn the page to read upside-down hints.
7. **Practice regularly**—proof writing requires both logical thinking and technical precision.
8. **Revisit challenging problems** after a few days to reinforce understanding and proof patterns.

### For Tutors

- Use Part 1 problems as fully worked examples in lessons, highlighting proof structure and logical flow.
- Assign Part 2 problems for homework or practice, encouraging students to attempt proofs before revealing hints.
- Focus on proof communication—clarity of expression and logical rigor are essential skills.
- Select problems by technique (direct, contradiction, induction, cases) to target specific proof methods.
- Use the variety of difficulty levels to differentiate instruction for different student abilities.
- Emphasize the Takeaways sections to help students extract generalizable techniques.

### For Educators

- Incorporate problems into lesson plans, assessment preparation, or enrichment activities.
- Emphasize systematic proof construction and clear communication of mathematical reasoning.
- Use problems to demonstrate when different proof techniques are most appropriate.
- Assign multi-part problems to develop sustained reasoning and proof-building skills.
- Connect proof techniques to other Extension 2 topics where rigorous arguments are required.

## Repository Layout

- `HSC-Proofs.tex`: Main LaTeX source with Introduction (including Proof Primer), Part 1, Part 2, and Conclusion.
- `Makefile`: Docker-based build automation with OS-specific PDF opening.
- `README.md`: Project overview (this file).
- `.gitignore`: Filters LaTeX artifacts, keeps `releases/HSC-Proofs.pdf`.
- `PLAN.md`: Comprehensive implementation plan with phases, tasks, and success criteria.
- `PROBLEM_CLASSIFICATION.md`: Detailed analysis of all 30 sample problems by difficulty, proof technique, topic, and pedagogical value.
- `SELECTION_SUMMARY.md`: Strategic selection justification for Part 1 and Part 2 problems with technique coverage verification.
- `samples/`: Original problem files (30 problems):
  - `00-basic.tex`: Fundamental number theory concepts and proof technique reference
  - `01.tex` through `30.tex`: Individual proof problems
- `problems/`: Organized problem files by part and number that are `\input` into main TeX:
  - **Part 1 (Detailed Solutions)**: `part1-01.tex` through `part1-15.tex` (complete with solutions and takeaways)
  - **Part 2 (Hints + Sketches)**: `part2-01.tex` through `part2-15.tex` (with hints and solution sketches)
- `solutions/`: Reserved for future standalone solution files.
- `styles/`: Shared LaTeX style files (copied from HSC-Induction):
  - `dl101-colors.sty`: Color palette (bookpurple, bookred, bookblack, softivory)
  - `dl101-hints.sty`: Upside-down hint environment for Part 2 problems
  - `dl101-hsc-problems.sty`: Problem, solution, and takeaways box environments
- `releases/`: Compiled PDFs (run `make release` to populate).

## Problem Distribution

### Part 1: Detailed Solutions (15 problems)

| Difficulty | Count | Topics Covered |
|------------|-------|----------------|
| Easy | 5 | Consecutive integers, difference of squares, simple divisibility, irrationality proofs |
| Medium | 5 | Modular arithmetic, biconditional proofs, parity arguments, conditional divisibility |
| Hard | 5 | Diophantine equations, nested radical induction, logarithm irrationality, complex divisibility |

### Part 2: Hints + Solution Sketches (15 problems) ✓ Complete

| Difficulty | Count | Topics Covered |
|------------|-------|----------------|
| Easy | 5 | Parity arguments (a³-a+1), rational+irrational sums, non-constructive existence, divisibility constraints, Mersenne contrapositive |
| Medium | 5 | Exponential divisibility, factorization (x²-y²=1), divisibility by 9 rule, complex number geometry, biconditional parity |
| Hard | 5 | Irrational products counterexample, Pythagorean parity contradiction, exponential inequalities, sandwich inequality induction, advanced divisibility induction |

## Proof Techniques Covered

### Direct Proof
- Starting from assumptions and deriving conclusion through logical steps
- Algebraic manipulation and substitution
- Using known properties and theorems
- **Problems**: 7 total across all difficulties

### Proof by Contradiction
- Assuming negation and deriving a contradiction
- Proving irrationality through reductio ad absurdum
- Logical impossibility arguments
- **Problems**: 8 total, especially for irrationality proofs

### Mathematical Induction
- Base case verification
- Inductive hypothesis and step
- Strong induction variants
- **Problems**: 6 total, including divisibility and nested radicals

### Proof by Cases
- Exhaustive case analysis (odd/even, remainder classes)
- Combining results from all cases
- Systematic consideration of scenarios
- **Problems**: 9 total, often combined with other techniques

## Key Topics Covered

- **Divisibility**: 10 problems covering multiples, factors, and divisibility rules
- **Irrationality**: 5 problems proving numbers cannot be expressed as fractions
- **Modular Arithmetic**: 6 problems using congruence and remainder analysis
- **Parity**: 4 problems exploiting odd/even properties
- **Logic**: 2 problems on logical structure and biconditionals
- **Mixed Techniques**: 3 problems requiring multiple approaches

## Author

Vu Hung Nguyen  
- LinkedIn: https://www.linkedin.com/in/nguyenvuhung/  
- GitHub: https://github.com/vuhung16au/  
- Repository: https://github.com/vuhung16au/math-olympiad-ml/tree/main/HSC-Proofs

---

Good luck with your HSC Mathematics Extension 2 studies and examinations!

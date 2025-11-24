


# Finish project on HSC Integrals

Folder: `/HSC-Integrals/`
Sample problems: 
- `/HSC-Integrals/samples/*.tex`

The objective of this project is to create a collection of HSC Math Extension 2 problems that are relevant to integrals. The problems should be suitable for HSC students.

Folder structure of this project (`/HSC-Integrals/`) is similar to `/HSC-Induction/`. E.g.
- Makefile 
- HSC-Integrals.tex
- samples/
- problems/
- solutions/
- styles/: use the same styles as `/HSC-Induction/styles/`
- releases/
- README.md
- .gitignore 

The content of the file `HSC-Integrals.tex` is as follows:
- Intro to this project
 Brief review of integrals fundamentals. Pls refer to `HSC-Integrals/samples/00-basic.tex` to cover basic integrals.
 Key theorems/formulas students should know (integration techniques, substitution, integration by parts, definite and indefinite integrals, etc.)
 Notation and conventions used in this project.


`README.md` should contain the following sections:
- Introduction
- What this project is about, the audience it is for
- How to build this project
- Conclusion & good luck!

# Key Integral Topics 

HSC Extension 2 questions on Integrals typically cover the following topics:

## Advanced Techniques of Integration

- Integration by Parts
- Partial Fractions
- Trigonometric Substitutions
- Rationalising Substitutions


## Reduction Formulae (Recurrence Relations)

- Derivation: Using Integration by Parts to find a relationship between $I_n$ and $I_{n-1}$ or $I_{n-2}$ (where $n$ is an integer). 
- Application: Using the derived formula to evaluate a specific integral (e.g., "Hence, evaluate $I_4$
- Proof by Induction: Occasionally combined with mathematical induction to prove a result about the integral for all $n$.

## 3. Volumes of Solids

- Method of Cylindrical Shells
- General Slicing (Cross-sections)

## Harder / Abstract Definite Integrals

- Properties of Definite Integrals. Exploiting symmetry (odd and even functions).
- Inequalities:Proving integral inequalities using the property: if $f(x) \le g(x)$ on $[a,b]$, then $\int_a^b f(x) \, dx \le \int_a^b g(x) \, dx$.Often linked with the Cauchy-Schwarz inequality in integral form.

# Target audience: 

Students who are preparing for HSC Math Extension 2 who want to challenge themselves with difficult problems and develop advanced problem-solving skills using Integrals.

Part 1: Problems and Solutions (Detailed solutions)
- (easy problems) Basic integral problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (medium problems) Medium integral problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (hard problems) Advanced integral problems: you pick 5 problems from the folder `samples/` and solve them in detail.
(Do not show Hints for problems in Part 1, just state the problems and show the solutions.)
So, that Part 1 has 3x5 = 15 problems.

Part 2: Problems and Solutions (less detailed solutions)
- (easy problems) Basic integral problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (medium problems) Medium integral problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (hard problems) Advanced integral problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
For problems in Part 2, show Hints for problems.
- Conclusion & good luck!

Part 1 and Part 2 aim for roughly equal distribution across difficulty levels (but not strictly necessary).

Note:
- We have about +60 sample problems in the folder `samples/`. You can pick any 3x5 problems from the folder `samples/` and solve them in detail.
- And you pick the rest of the problems and solve them (less detailed solutions).
- Make sure no problem is repeated in Part 1 and Part 2.

The structure (Sections) of the file `README.md` is similar to `/HSC-Induction/README.md` but about this project.

Difficulty criteria for easy/medium/hard classifications:
- Easy: Direct application of formulas (basic integration techniques, substitution, etc.)
- Medium: Multi-step problems combining 2-3 concepts
- Hard: Problems requiring creative approaches, proofs, or multiple complex techniques, often involving reduction formulae or advanced applications.
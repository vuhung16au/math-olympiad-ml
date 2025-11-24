


# Finish project on HSC Mechanics

Folder: `/HSC-Mechanics/`
Sample problems: 
- `/HSC-Mechanics/samples/*.tex`
The objective of this project is to create a collection of HSC Math Extension 2 problems that are relevant to mechanics. The problems should be suitable for HSC students.

Folder structure of this project (`/HSC-Mechanics/`) is similar to `/HSC-Induction/`. E.g.
- Makefile 
- HSC-Mechanics.tex
- samples/
- problems/
- solutions/
- styles/: use the same styles as `/HSC-Induction/styles/`
- releases/
- README.md
- .gitignore 
- `PROBLEM_CLASSIFICATION.md`: similar to `/HSC-Integrals/PROBLEM_CLASSIFICATION.md`, but for mechanics problems.
- `SELECTION_SUMMARY.md`: similar to `/HSC-Integrals/SELECTION_SUMMARY.md`, but for mechanics problems.

The content of the file `HSC-Mechanics.tex` is as follows:
- Intro to this project
 Brief review of mechanics fundamentals. Pls refer to `HSC-Mechanics/samples/00-basic.tex` to cover basic mechanics.
 Key theorems/formulas students should know (Newton's laws, kinematics equations, work-energy theorem, momentum, etc.)
 Notation and conventions used in this project.


`README.md` should contain the following sections:
- Introduction
- What this project is about, the audience it is for
- How to build this project
- Conclusion & good luck!

# Key Mechanics Topics 

HSC Math Extension 2 questions on Mechanics typically cover the following topics:


| Topic | Common Task | Key Mathematical Skill |
| :--- | :--- | :--- |
| **SHM** | Find the center of motion and period. | Trigonometry & Differentiation |
| **Variable Force** | Find $v$ given $x$. | Integration using $a = \frac{d}{dx}(\frac{1}{2}v^2)$ |
| **Resisted Motion** | Find time to reach max height. | Integration using partial fractions |
| **Terminal Velocity** | Find limit as $t \to \infty$. | Limits & Understanding $a=0$ |

# Target audience: 

Students who are preparing for HSC Math Extension 2 who want to challenge themselves with difficult problems and develop advanced problem-solving skills using Mechanics.

Part 1: Problems and Solutions (Detailed solutions)
- (easy problems) Basic Mechanics problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (medium problems) Medium Mechanics problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (hard problems) Advanced Mechanics problems: you pick 5 problems from the folder `samples/` and solve them in detail.
(Do not show Hints for problems in Part 1, just state the problems and show the solutions.)
So, that Part 1 has 3x5 = 15 problems.

Part 2: Problems and Solutions (less detailed solutions)
- (easy problems) Basic Mechanics problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (medium problems) Medium Mechanics problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (hard problems) Advanced Mechanics problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
For problems in Part 2, show Hints for problems.
- Conclusion & good luck!

Part 1 and Part 2 aim for roughly equal distribution across difficulty levels (but not strictly necessary).

Notes:
- We have about +60 sample problems in the folder `samples/`. You can pick any 3x5 problems from the folder `samples/` and solve them in detail.
- And you pick the rest of the problems and solve them (less detailed solutions).
- Make sure no problem is repeated in Part 1 and Part 2.
- A problem in a file `samples/XX.tex` can have multiple sub-questions (a), (b), (c), etc. You can choose to include all sub-questions and solutions included
- Use the same problems/solutions in `samples/XX.tex` files, do not create new problems/solutions (if you have to, only minor modifications are allowed, e.g. change numerical values, etc) and inform me.
- Some problems in `samples/*.tex` may have tikz diagrams. When you mirror the problems to the project, make sure include the tikz diagrams as well.

The structure (Sections) of the file `README.md` is similar to `/HSC-Induction/README.md` but about this project.

Difficulty criteria for easy/medium/hard classifications:
- Easy: Direct application of formulas (basic mechanics techniques, substitution, etc.)
- Medium: Multi-step problems combining 2-3 concepts
- Hard: Problems requiring creative approaches, proofs, or multiple complex techniques, often involving reduction formulae or advanced applications.



# Finish project on HSC Complex Numbers

Folder: `/HSC-ComplexNumbers/`
Sample problems: 
- `/HSC-ComplexNumbers/samples/`
- `/HSC-ComplexNumbers/samples/gemini-hard-complex.md`
- `/HSC-ComplexNumbers/samples/sample-questions-complex.tex`

The objective of this project is to create a collection of HSC Math Extension 2 problems that are relevant to complex numbers. The problems should be suitable for HSC students.

Folder structure of this project (`/HSC-ComplexNumbers/`) is similar to `/HSC-Induction/`. E.g.

- Makefile 
- HSC-ComplexNumbers.tex
- samples/
- problems/
- solutions/
- styles/: use the same styles as `/HSC-Induction/styles/`
- releases/
- README.md
- .gitignore

The content of the file `HSC-ComplexNumbers.tex` is as follows:

- Intro to this project
 Brief review of complex number fundamentals
 Key theorems/formulas students should know
 Notation and conventions used in this project.


# Key Complex Numbers Topics 

HSC Extension 2 questions on complex numbers typically cover the following topics:

## 1. Forms and Conversions
- **Cartesian, Polar, and Exponential Forms**: Converting between \(x+iy\), \(r(\cos \theta +i\sin \theta )\), and \(re^{i\theta }\)
- **Modulus and Argument**: Finding \(|z|\) and \(\arg(z)\) and their properties

## 2. Fundamental Theorems
- **Euler's Theorem**: \(e^{i\theta} = \cos\theta + i\sin\theta\) and applications
- **De Moivre's Theorem**: \((r(\cos\theta + i\sin\theta))^n = r^n(\cos(n\theta) + i\sin(n\theta))\)
  - Finding powers of complex numbers
  - Finding \(n\)-th roots of complex numbers
  - Proving trigonometric identities

## 3. Argand Diagram and Geometry
- **Sketching Regions and Loci**: Interpreting inequalities and equations geometrically (e.g., \(|z+2|\ge 2\), \(|z-1| = |z+i|\))
- **Curves in the Complex Plane**: Circles, lines, rays, and more complex curves
- **Geometric Transformations**: Rotation, reflection, scaling, and translation using complex multiplication and addition

## 4. Polynomials and Equations
- **Quadratic Equations**: Solving equations with complex coefficients
- **Polynomial Roots**: Finding and using properties of roots (sum, product, conjugate pairs)
- **Factorization**: Using complex roots to factor polynomials over \(\mathbb{C}\)

## 5. Vector and Geometric Applications
- **Complex Numbers as Vectors**: Using complex arithmetic to solve geometric problems
- **Distance and Midpoint**: Interpreting \(|z_1 - z_2|\) and \(\frac{z_1 + z_2}{2}\) geometrically
- **Rotation and Scaling**: Applying geometric transformations using multiplication by complex numbers

- Target audience: students who are preparing for HSC Math Extension 2 who want to challenge themselves with difficult problems and develop advanced problem-solving skills using complex numbers.

Part 1: Problems and Solutions (Detailed solutions)
- (easy problems) Basic complex numbers problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (medium problems) Medium complex numbers problems: you pick 5 problems from the folder `samples/` and solve them in detail.
- (hard problems) Advanced complex numbers problems: you pick 5 problems from the folder `samples/` and solve them in detail.
(Do not show Hints for problems in Part 1, just state the problems and show the solutions.)
So, that Part 1 has 3x5 = 15 problems.

Part 2: Problems and Solutions (less detailed solutions)
- (easy problems) Basic complex numbers problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (medium problems) Medium complex numbers problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
- (hard problems) Advanced complex numbers problems: you pick problems from the folder `samples/` and solve them (less detailed solutions)
For problems in Part 2, show Hints for problems.
- Conclusion & good luck!

Part 1 and Part 2 aim for roughly equal distribution across difficulty levels.

Note:
- We have about 64 sample problems in the folder `samples/`. You can pick any 3x5 hav from the folder `samples/` and solve them in detail.
- And you pick the rest of the problems and solve them (less detailed solutions).
- Make sure no problem is repeated in Part 1 and Part 2.

The structure (Sections) of the file `README.md` is similar to `/HSC-Induction/README.md` but about this project.


Difficulty criteria for easy/medium/hard classifications:
- Easy: Direct application of formulas (De Moivre, conversions, simple loci)
- Medium: Multi-step problems combining 2-3 concepts
- Hard: Problems requiring creative approaches, proofs, or multiple complex techniques
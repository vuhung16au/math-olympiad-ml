# HSC Mathematics Extension 1: Combinatorics Practice

## Attribution
© 2026 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2026). math-olympiad-ml — HSC-Combinatorics. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This booklet curates combinatorics problems for NSW HSC Mathematics Extension 1 students. It focuses on counting principles, permutations, combinations, circular arrangements, committee selection, and basic probability in a style suitable for HSC preparation.

## Licensing
Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

Software/code remains MIT-licensed per the repository root LICENSE.

## Overview

The booklet [`HSC-Combinatorics.tex`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/HSC-Combinatorics.tex) contains:

- A short introduction to the core counting tools used in the HSC syllabus
- A Part 1 problem set with concise worked solutions
- A placeholder Part 2 section for future expansion with more short-answer practice

The initial problem set is based on [`TODO/combinations.md`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/TODO/combinations.md).

## Topics Covered

- Fundamental counting principle
- Permutations with and without repeated letters
- Circular arrangements
- Combinations and committee selection
- Simple selection probability
- Interpreting counting questions carefully from their wording

## How to Build the PDF

### Using Docker

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Combinatorics.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Combinatorics.tex
```

### Using Make

```bash
make pdf
make open
```

## Repository Layout

- [`HSC-Combinatorics.tex`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/HSC-Combinatorics.tex): Main LaTeX source
- [`problems/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/problems): Problem snippets grouped by difficulty
- [`styles/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/styles): Shared LaTeX styles copied from the existing HSC booklet format
- [`TODO/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/TODO): Notes for future problem expansion
- [`releases/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Combinatorics/releases): Release PDF output

## Notes

One source problem about license plates is internally inconsistent: a format of two digits, then two letters, then two digits cannot produce the plate `COP789`. In the current booklet, that part is handled explicitly as a reading-check question, so the probability under the stated format is `0`.

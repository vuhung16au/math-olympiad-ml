# HSC Mathematics Extension 1: Probability

## Attribution
© 2026 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2026). math-olympiad-ml — HSC-Probability. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This booklet is a structured probability practice resource for NSW HSC Mathematics Extension 1 students. It combines core event-based probability with discrete probability distributions in the same house style as the existing `HSC-XXX` booklets in this repository.

## Overview

The booklet [`HSC-Probability.tex`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Probability/HSC-Probability.tex) contains:

- a concise fundamentals review for key rules, notation, and models
- `Part 1` detailed worked solutions that model clean HSC-style reasoning
- `Part 2` additional questions with upside-down hints and concise solutions

The content stays within the HSC Mathematics Extension 1 level and intentionally excludes Extension 2 continuous probability material.

## Topics Covered

- sample spaces and equally likely outcomes
- complements, unions, intersections, and Venn-style reasoning
- addition rule and multiplication rule
- conditional probability and independence
- counting-based probability
- discrete random variables
- expected value and variance
- binomial distributions

## How to Build the PDF

### Using Docker

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Probability.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Probability.tex
```

### Using Make

```bash
make pdf
make open
```

## Repository Layout

- [`HSC-Probability.tex`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Probability/HSC-Probability.tex): Main LaTeX source
- [`problems/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Probability/problems): Primer and problem-bank files grouped by difficulty
- [`styles/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Probability/styles): Shared LaTeX styling used across the booklet
- [`releases/`](/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Probability/releases): PDF output

## Notes

- The booklet combines the natural Extension 1 sequence of `Probability` and `Discrete probability distributions`.
- The progression is concept-driven rather than page-by-page textbook imitation.
- Binomial distribution is treated as the capstone discrete model for repeated independent trials.

## Licensing

Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

Software/code remains MIT-licensed per the repository root LICENSE.

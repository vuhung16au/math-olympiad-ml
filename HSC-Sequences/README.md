# HSC Mathematics Extension 1: Sequences and Series

## Attribution
© 2026 Vu Hung Nguyen
Preferred attribution: "Vu Hung Nguyen (2026). math-olympiad-ml - HSC-Sequences. Available at https://github.com/vuhung16au/math-olympiad-ml/"

This booklet is a structured sequences and series practice resource for NSW HSC Mathematics Extension 1 students. It follows the same project layout and house style as other HSC booklets in this repository.

## Overview

The booklet [HSC-Sequences.tex](HSC-Sequences.tex) contains:

- front matter with title page, QR page, quote page, and table of contents
- an introduction and a fundamentals review
- Part 1 detailed worked solutions
- Part 2 additional questions with upside-down hints and concise solutions
- appendices for formulas and common traps

## Topics Covered

- sequences and notation
- arithmetic sequences and arithmetic series
- geometric sequences and geometric series
- solving AP and GP problems
- sigma notation and finite sums
- limiting sum of a geometric series
- recurring decimals and geometric series

## How to Build the PDF

### Using Docker

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Sequences.tex
docker run --rm -v "$(pwd):/workdir" -w /workdir texlive/texlive:latest \
    pdflatex -interaction=nonstopmode HSC-Sequences.tex
```

### Using Make

```bash
make pdf
make open
```

## Repository Layout

- [HSC-Sequences.tex](HSC-Sequences.tex): main LaTeX source
- [problems/](problems): modular content files grouped by section
- [styles/](styles): shared LaTeX styling
- [releases/](releases): PDF output

## Licensing

Non-code content in this folder is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). See [LICENSE.md](LICENSE.md).

Software and code remain MIT-licensed per the repository root LICENSE.

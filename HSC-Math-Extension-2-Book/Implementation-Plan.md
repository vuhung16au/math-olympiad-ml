# HSC-Math-Extension-2-Book Implementation Plan

This document captures the agreed requirements and the remaining decision on the final book title. No implementation has been started yet.

## Agreed Structure

`HSC-Math-Extension-2-Book` should mirror the clean publishable structure of `HSC-LastResorts`, using this as the source of truth:

```text
HSC-Math-Extension-2-Book.tex
fonts/
LICENSE.md
Makefile
problems/
README.md
releases/
solutions/
styles/
```

When mirroring `HSC-LastResorts`, ignore these extra folders:

- `samples/`
- `samples2/`
- `Prompts/`

## Makefile Requirements

The `Makefile` should mirror the `HSC-LastResorts` targets:

- `all` - Build the main PDF (default)
- `pdf` - Compile `.tex` file to `.pdf`
- `clean` - Remove build artifacts
- `release` - Build and move PDF to `releases/`
- `final` - Clean, build PDF, and release
- `help` - Show this help message

## Main Book Structure

The main file should be `HSC-Math-Extension-2-Book.tex`.

It should mirror the structure of `HSC-LastResorts` with:

- Title page
- Copyright notice
- Preface
- Table of contents
- Part title pages
- Booklet-as-chapter structure

There should be no alphabetical index. Use a table of contents only.

## Title Page Requirements

Title page format:

`HSC Maths Extension 2 - Core, Enrichment and Last Resorts`

Author:

`Vu Hung Nguyen`

Copyright:

`Vu Hung Nguyen, 2025`

License note:

`This work is licensed under CC BY 4.0, see the LICENSE file on the github page for more info.`

## Book Title

Title:
`Master Book`

So the full title would be:

`HSC Maths Extension 2 - Core, Enrichment and Last Resorts`


## Agreed Part Titles

Part 1:

`Core Theory and Techniques`

Part 2:

`Advanced Methods and Enrichment`

Part 3:

`Curated HSC Problem Sets`

Part 4:

`The Last Resorts`

## Chapter Order

### Part 1: Core Theory and Techniques

- `HSC-Proofs`
- `HSC-Vectors`
- `HSC-ComplexNumbers`
- `HSC-Integrals`
- `HSC-Mechanics`

### Part 2: Advanced Methods and Enrichment

- `HSC-Induction`
- `HSC-Inequalities`
- `HSC-Polynomials`

### Part 3: Curated HSC Problem Sets

- `HSC-Collections`
  - subtitle/description: `A curated collection of HSC problems`

### Part 4: The Last Resorts

- `HSC-LastResorts`

## Content Reuse Strategy

Use the existing booklet sources as much as possible.

Preferred approach:

- reuse existing LaTeX content via `\input` or `\include` where practical
- normalize paths where needed
- adapt styles only when necessary to produce a unified build
- avoid rewriting booklet content unless integration requires it


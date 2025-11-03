# Project Instructions

This repository contains a book on neural networks written in LaTeX. The book targets undergraduate students and is intentionally friendly for advanced high‑school readers.

## Language and Style
- Use British English (Australian spelling) throughout the manuscript and code comments.
- Ensure headings use English terms (e.g., "Chapter 5", not Vietnamese forms).
- Follow the existing colour scheme and font family defined in `styles/`.
 - Favour clarity over formality; keep sentences short and approachable.
 - Use metaphors, concrete examples, and visualisations to explain concepts.

## LaTeX Workflow
- Build locally with `make pdf`. Artifacts are written to `release/`.
- Preview with `make view` and clean with `make clean`.
- Use the style packages in `styles/` via `main.tex`. Do not reintroduce duplicate packages already provided by styles.
 - All LaTeX sources live under `chapters/`, with styles under `styles/`. Always apply styles from `styles/` to maintain consistency.

## Branching and Commits
- Create feature branches from `main`: `feature/<short-topic>` or `fix/<short-topic>`.
- Commit messages:
  - Title (≤72 chars): imperative mood (e.g., "Add theorem boxes")
  - Body: what/why, not how; reference files like `chapters/04-Linear-Models.tex`.

## Pull Requests
- Keep PRs focused and reviewable (< ~300 lines diff preferred).
- Ensure `make pdf` succeeds before requesting review.
- Include screenshots or PDF page snippets for visual changes when relevant.

## Content Guidelines
- Prefer `theorem`, `definition`, `example`, `remark`, and `keytakeaways` environments from styles.
- Use `learningobjectives` and `exercisebox`/`hintbox` for pedagogy.
- Embed figures in `images/`, reference with `\includegraphics{}`.
 - Aim for accessibility: define terms on first use, provide intuition before formalism, and show minimal working examples before generalisations.
 - When possible, provide visual aids (plots, diagrams) to reinforce the text.
 - TikZ in LaTeX to draw diagrams, graphs, and other visualizations when possible.

## Licensing and Attribution
- Licensed under CC BY 4.0. Attribute "Vu Hung Nguyen" when reusing content.
- Include citation entries in `references/references.bib`; compile references via standard LaTeX flow.

## Filing Issues
- Use Issues for bugs/requests. Provide:
  - Reproduction steps (`make pdf` log excerpt if build-related).
  - Affected files (e.g., `chapters/07-Loss-and-Optimization.tex`).
  - Expected vs actual behaviour.


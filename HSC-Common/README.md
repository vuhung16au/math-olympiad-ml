# HSC-Common

Shared resources for the HSC booklet LaTeX projects: style files (`.sty`), fonts, images, and contact metadata.

## Layout

- **`styles/`** — `\usepackage{dl101-*}` packages. Each booklet adds `../HSC-Common/styles/` to `\input@path` and sets `\HSCBookletHeaderTitle` before loading `dl101-layout`.
- **`fonts/`** — Shared fonts (e.g. `SAMAN___.TTF` for `fontspec`).
- **`assets/`** — Shared images (e.g. title-page backgrounds).
- **`contact.md`** — Maintainer links for reuse in booklets.

## Booklet header title

In the main `.tex` file, after `\documentclass` and the `\input@path` snippet:

```latex
\newcommand{\HSCBookletHeaderTitle}{Your Short Title}
\usepackage{dl101-layout}
```

## Takeaways lists

Some booklets wrap `takeaways` in an implicit `itemize` (when entries use `\item` directly inside `takeaways`). Use the package option:

```latex
\usepackage[takeawaysitemize]{dl101-hsc-problems}
```

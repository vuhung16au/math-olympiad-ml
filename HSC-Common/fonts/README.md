## Samarkan font (optional)

This project uses the **Samarkan** TrueType font for the `\ramanujanfont` macro (see `HSC-LastResorts.tex`). If the font file is not present, the PDF will still compile, but `\ramanujanfont` will have no effect under pdfLaTeX.

## How to get the font

- **Download**: get “Samarkan Font” from `https://www.fontmagic.com/samarkan.font` or `https://www.dafont.com/font-comment.php?file=samarkan`
- **Place it here**: copy the `.ttf` into this folder: `HSC-LastResorts/fonts/`
- **Filename expected by the TeX source**: `SAMAN___.TTF` (keep this exact name)

You can either keep the font file only in this `fonts/` folder (recommended), or also install it system-wide (optional).

## How to compile (embed the font)

This font is loaded via `fontspec`, so you must compile with **LuaLaTeX** (or XeLaTeX).

From `HSC-LastResorts/`:

- **Makefile (recommended)**:
  - `make`
- **Direct command**:
  - `lualatex HSC-LastResorts.tex` (run twice for TOC/cross-refs)

## Licensing note (important)

Samarkan is **shareware / not freely usable**. That’s why this repository **cannot distribute** the font file; you must download and use it under the font’s own license/terms.
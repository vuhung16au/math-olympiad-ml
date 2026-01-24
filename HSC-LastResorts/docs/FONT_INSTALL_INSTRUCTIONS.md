# Font Installation Instructions

## Font Installation (Already Done)
The Samarkan font has been installed to: `~/.local/share/fonts/SAMAN___.TTF`

## Required LaTeX Packages

To use TTF fonts in LaTeX, you need to install the following packages:

```bash
sudo apt-get update
sudo apt-get install texlive-luatex texlive-fonts-extra
```

Or if you prefer XeLaTeX:
```bash
sudo apt-get install texlive-xetex
```

## Current Configuration

The Makefile has been updated to use `lualatex` instead of `pdflatex` to support TTF fonts.

The font is configured in `HSC-LastResorts.tex` and applied to:
- Problem title: "The Ramanujan Summation & Filters"
- "The Indian mathematician Srinivasa Ramanujan"
- "Ramanujan" in part (b)

## After Installing Packages

Once you've installed the required packages, run:
```bash
make pdf
```

The Samarkan font will be used for the specified text in the Ramanujan problem.

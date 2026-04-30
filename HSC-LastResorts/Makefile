# Makefile for HSC-LastResorts

TEX=HSC-LastResorts.tex

# Font support: allow TrueType/OpenType via fontspec.
# Use LuaLaTeX so fonts/SAMAN___.TTF can be embedded.
LATEX=lualatex
LATEXFLAGS=-interaction=nonstopmode -halt-on-error -file-line-error

# Two passes: \tableofcontents and cross-refs read .toc/.aux written at end of pass 1.
all pdf:
	$(LATEX) $(LATEXFLAGS) $(TEX)
	$(LATEX) $(LATEXFLAGS) $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.pdf

release: pdf
	mv HSC-LastResorts.pdf releases/

final: clean release
open:
	open HSC-LastResorts.pdf

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build PDF (2 passes) and move to releases/"
	@echo "  final   - Clean, then release (2 LaTeX runs total)"
	@echo "  help    - Show this help message"

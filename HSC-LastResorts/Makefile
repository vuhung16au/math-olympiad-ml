# Makefile for HSC-LastResorts

TEX=HSC-LastResorts.tex

# Font support: allow TrueType/OpenType via fontspec.
# Use LuaLaTeX so fonts/SAMAN___.TTF can be embedded.
LATEX=lualatex
LATEXFLAGS=-interaction=nonstopmode -halt-on-error -file-line-error


all:
	$(LATEX) $(LATEXFLAGS) $(TEX)
	$(LATEX) $(LATEXFLAGS) $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.pdf

release:
	$(LATEX) $(LATEXFLAGS) $(TEX)
	mv HSC-LastResorts.pdf releases/
final: clean pdf release
open:
	open HSC-LastResorts.pdf
pdf:
	$(LATEX) $(LATEXFLAGS) $(TEX)

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build and move PDF to releases/"
	@echo "  final   - Clean, build PDF, and release"
	@echo "  help    - Show this help message"

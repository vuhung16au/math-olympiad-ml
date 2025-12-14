# Makefile for HSC-LastResorts

LATEX=pdflatex
TEX=HSC-LastResorts.tex

all:
	$(LATEX) $(TEX)
	$(LATEX) $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.pdf

release:
	$(LATEX) $(TEX)
	mv HSC-LastResorts.pdf releases/
final: clean pdf release
open:
	open HSC-LastResorts.pdf
pdf:
	$(LATEX) $(TEX)

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build and move PDF to releases/"
	@echo "  final   - Clean, build PDF, and release"
	@echo "  help    - Show this help message"

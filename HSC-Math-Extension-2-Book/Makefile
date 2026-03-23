# Makefile for HSC-Math-Extension-2-Book

TEX=HSC-Math-Extension-2-Book.tex
PDF=HSC-Math-Extension-2-Book.pdf

# Default to pdfLaTeX for portability in the combined wrapper book.
# The folder still mirrors HSC-LastResorts assets, including fonts/.
LATEX=pdflatex
LATEXFLAGS=-interaction=nonstopmode -halt-on-error -file-line-error

all:
	$(LATEX) $(LATEXFLAGS) $(TEX)
	$(LATEX) $(LATEXFLAGS) $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.pdf

release:
	$(LATEX) $(LATEXFLAGS) $(TEX)
	mv $(PDF) releases/

final: clean pdf release

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

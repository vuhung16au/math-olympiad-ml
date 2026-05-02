# Makefile for HSC-Math-Extension-2-Book

TEX=HSC-Math-Extension-2-Book.tex
PDF=HSC-Math-Extension-2-Book.pdf

# Build with latexmk (pdfLaTeX) so references and bibliographies resolve automatically.
LATEXMK=latexmk
LATEXMKFLAGS=-pdf -interaction=nonstopmode -halt-on-error -file-line-error

all:
	$(LATEXMK) $(LATEXMKFLAGS) $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.fdb_latexmk *.fls *.synctex.gz *.pdf

release:
	$(LATEXMK) $(LATEXMKFLAGS) $(TEX)
	mv $(PDF) releases/

final: clean pdf release

pdf:
	$(LATEXMK) $(LATEXMKFLAGS) $(TEX)

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build and move PDF to releases/"
	@echo "  final   - Clean, build PDF, and release"
	@echo "  help    - Show this help message"

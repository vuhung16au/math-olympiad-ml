# Makefile for HSC-LastResorts

TEX=HSC-LastResorts.tex

# Font support: allow TrueType/OpenType via fontspec.
# latexmk drives LuaLaTeX so fonts/SAMAN___.TTF can be embedded; runs until aux is stable.
LATEXMK=latexmk
LATEXMKFLAGS=-lualatex -interaction=nonstopmode -halt-on-error -file-line-error

all pdf:
	$(LATEXMK) $(LATEXMKFLAGS) $(TEX)

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
	@echo "  release - Build PDF (latexmk) and move to releases/"
	@echo "  final   - Clean, then release"
	@echo "  help    - Show this help message"

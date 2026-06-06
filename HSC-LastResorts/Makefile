# Makefile for HSC-LastResorts

TEX=HSC-LastResorts.tex
STEM=$(TEX:.tex=)

# Font support: allow TrueType/OpenType via fontspec.
# latexmk drives LuaLaTeX so fonts/SAMAN___.TTF can be embedded; runs until aux is stable.
LATEXMK=latexmk
LATEXMKFLAGS=-lualatex -interaction=nonstopmode -halt-on-error -file-line-error

all pdf:
	@if [ -f $(STEM).aux ] && grep -q $$'\x00' $(STEM).aux 2>/dev/null; then \
		echo "Removing corrupted $(STEM).aux"; \
		rm -f $(STEM).aux $(STEM).out $(STEM).toc $(STEM).fdb_latexmk $(STEM).fls; \
	fi
	$(LATEXMK) $(LATEXMKFLAGS) $(TEX)

clean:
	-$(LATEXMK) -C
	rm -f $(STEM).aux $(STEM).log $(STEM).out $(STEM).toc
	rm -f $(STEM).fdb_latexmk $(STEM).fls $(STEM).synctex.gz $(STEM).pdf

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

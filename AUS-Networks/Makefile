# Makefile for AUS-Networks

TEX=AUS-Networks.tex
STEM=$(TEX:.tex=)
RELEASE=AUS-Networks.pdf

LATEXMK=latexmk
LATEXMKFLAGS=-lualatex -interaction=nonstopmode -halt-on-error -file-line-error

DOCKER_RUN=docker run --rm -v "$$PWD":/workdir -v "$$PWD/../HSC-Common":/HSC-Common -w /workdir texlive/texlive:latest

.PHONY: all pdf clean release final open help

all: pdf

pdf:
	@if [ -f $(STEM).aux ] && grep -q $$'\x00' $(STEM).aux 2>/dev/null; then \
		echo "Removing corrupted $(STEM).aux"; \
		rm -f $(STEM).aux $(STEM).out $(STEM).toc $(STEM).fdb_latexmk $(STEM).fls; \
	fi
	$(DOCKER_RUN) $(LATEXMK) $(LATEXMKFLAGS) $(TEX)

clean:
	-$(DOCKER_RUN) $(LATEXMK) -C $(TEX)
	rm -f $(STEM).aux $(STEM).log $(STEM).out $(STEM).toc
	rm -f $(STEM).fdb_latexmk $(STEM).fls $(STEM).synctex.gz $(STEM).pdf

release: pdf
	mkdir -p releases
	cp $(STEM).pdf releases/$(RELEASE)

final: clean release

open: pdf
	open $(STEM).pdf

help:
	@echo "Available targets:"
	@echo "  all     - Build the AUS-Networks PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build PDF (latexmk) and move to releases/"
	@echo "  final   - Clean, then release"
	@echo "  open    - Build and open the AUS-Networks PDF"
	@echo "  help    - Show this help message"
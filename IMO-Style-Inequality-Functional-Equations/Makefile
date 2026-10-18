TEX=IMO-Style-Inequality-Functional-Equations.tex
STEM=$(TEX:.tex=)
LATEXMK=latexmk
LATEXMKFLAGS=-lualatex -interaction=nonstopmode -halt-on-error -file-line-error
DOCKER_RUN=docker run --rm -v "$$PWD":/workdir -v "$$PWD/../HSC-Common":/HSC-Common -w /workdir texlive/texlive:latest

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
  OPEN_CMD = open
else ifeq ($(UNAME_S),Linux)
  OPEN_CMD = xdg-open
else
  OPEN_CMD = start
endif

.PHONY: all pdf clean release final open help

all pdf:
	$(DOCKER_RUN) $(LATEXMK) $(LATEXMKFLAGS) $(TEX)
	@test -f $(STEM).pdf

clean:
	-$(DOCKER_RUN) $(LATEXMK) -C
	rm -f $(STEM).aux $(STEM).log $(STEM).out $(STEM).toc $(STEM).fdb_latexmk $(STEM).fls $(STEM).synctex.gz $(STEM).pdf

release: pdf
	mkdir -p releases
	cp $(STEM).pdf releases/

final: clean release

open: pdf
	$(OPEN_CMD) $(STEM).pdf

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Build PDF (latexmk) and copy to releases/"
	@echo "  final   - Clean, then release"
	@echo "  open    - Compile if needed, then open the PDF"
	@echo "  help    - Show this help message"
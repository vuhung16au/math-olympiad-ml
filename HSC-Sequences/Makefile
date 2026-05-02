TEXFILE = HSC-Sequences
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = releases

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	OPEN_CMD = open
else ifeq ($(UNAME_S),Linux)
	OPEN_CMD = xdg-open
else
	OPEN_CMD = start
endif

.PHONY: all pdf clean release open final help

all: pdf

pdf:
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -interaction=nonstopmode -file-line-error $(TEXFILE).tex; \
	else \
		docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
			latexmk -pdf -interaction=nonstopmode -file-line-error $(TEXFILE).tex; \
	fi
	@test -f $(PDFFILE)

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).log $(TEXFILE).out $(TEXFILE).toc $(TEXFILE).pdf \
		$(TEXFILE).fdb_latexmk $(TEXFILE).fls

release: pdf
	mkdir -p $(RELEASE_DIR)
	cp $(PDFFILE) $(RELEASE_DIR)/

open: pdf
	$(OPEN_CMD) $(PDFFILE)

final: clean pdf release

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile PDF (local latexmk, or Docker fallback)"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Copy PDF to releases/"
	@echo "  open    - Open the generated PDF"
	@echo "  final   - Clean, build PDF, and release"
	@echo "  help    - Show this help message"
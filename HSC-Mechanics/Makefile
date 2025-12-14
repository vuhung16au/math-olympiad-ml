TEXFILE = HSC-Mechanics
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = releases

# Build mode: USE_DOCKER=1 (default) runs TeX inside Docker,
# set USE_DOCKER=0 to use local latexmk installation.
USE_DOCKER = 0

# Detect OS for opening PDFs
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

pdf: $(PDFFILE)

$(PDFFILE): $(TEXFILE).tex
ifeq ($(USE_DOCKER),1)
	docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
		latexmk -pdf -interaction=nonstopmode -halt-on-error $(TEXFILE).tex
else
	latexmk -pdf -interaction=nonstopmode -halt-on-error $(TEXFILE).tex
endif

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).log $(TEXFILE).out $(TEXFILE).toc $(TEXFILE).pdf \
	       $(TEXFILE).fdb_latexmk $(TEXFILE).fls

release: $(PDFFILE)
	mkdir -p $(RELEASE_DIR)
	cp $(PDFFILE) $(RELEASE_DIR)/

open: $(PDFFILE)
	$(OPEN_CMD) $(PDFFILE)

final: clean pdf release

help:
	@echo "Available targets:"
	@echo "  all     - Build the main PDF (default)"
	@echo "  pdf     - Compile .tex file to .pdf (Docker by default)"
	@echo "  clean   - Remove build artifacts"
	@echo "  release - Copy PDF to releases/"
	@echo "  open    - Open the generated PDF"
	@echo "  final   - Clean, build PDF, and release"
	@echo "  help    - Show this help message"
	@echo ""
	@echo "Flags:"
	@echo "  USE_DOCKER=0  Use local latexmk instead of Docker"

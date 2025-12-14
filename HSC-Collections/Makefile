TEXFILE = HSC-Collections
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = releases

.PHONY: all pdf clean release help final

all: pdf

pdf:
	# Prefer local TeX Live if available; fallback to Docker
	@if command -v pdflatex >/dev/null 2>&1; then \
		pdflatex -interaction=nonstopmode $(TEXFILE).tex || true; \
		pdflatex -interaction=nonstopmode $(TEXFILE).tex || true; \
	else \
		docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
			pdflatex -interaction=nonstopmode $(TEXFILE).tex || true; \
		docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
			pdflatex -interaction=nonstopmode $(TEXFILE).tex || true; \
	fi
	@test -f $(PDFFILE)

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).log $(TEXFILE).out $(TEXFILE).toc $(TEXFILE).pdf

release: $(PDFFILE)
	mkdir -p $(RELEASE_DIR)
	cp $(PDFFILE) $(RELEASE_DIR)/

# Final target: clean, build, and release
final: clean pdf release

# Help target: list available commands
help:
	@echo "Make targets for HSC-Collections:"
	@echo "  make pdf      - Build the PDF (runs pdflatex twice)"
	@echo "  make clean    - Remove build artifacts and the PDF"
	@echo "  make release  - Copy built PDF to releases/"
	@echo "  make all      - Alias for 'make pdf'"
	@echo "  make final    - Clean, build PDF, then copy to releases/"


TEX=main.tex
OUT=release/Manifold.pdf
RELEASE_OUT=release/Manifold-Generative-AI.pdf
# Gather LaTeX sources to trigger rebuilds when chapters or parts change
SOURCES=$(TEX) \
        $(wildcard chapters/*.tex) \
        $(wildcard frontmatter/*.tex) \
        $(wildcard appendices/*.tex) \
        $(wildcard backmatter/*.tex) \
        $(wildcard styles/*.sty) \
        $(wildcard references/*.bib)

all: $(OUT)
pdf: $(OUT)

$(OUT): $(SOURCES)
	mkdir -p release
	latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=release main.tex
	@if [ -f release/main.pdf ]; then mv release/main.pdf $(OUT); fi

release: $(RELEASE_OUT)

$(RELEASE_OUT): $(SOURCES)
	mkdir -p release
	latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=release main.tex
	@if [ -f release/main.pdf ]; then cp release/main.pdf $(RELEASE_OUT); echo "Release PDF generated: $(RELEASE_OUT)"; fi

clean:
	latexmk -C -output-directory=release
	rm -f $(OUT) $(RELEASE_OUT)

view: pdf
	open $(OUT)

help:
	@echo "Available targets:"
	@echo "  make pdf     - Build the PDF from LaTeX sources"
	@echo "  make release - Build the release PDF (Manifold-Generative-AI.pdf)"
	@echo "  make view    - Build and open the PDF in the default viewer"
	@echo "  make clean   - Remove build artifacts and the generated PDFs"
	@echo "  make help    - Show this help message"

.PHONY: all clean pdf release view help

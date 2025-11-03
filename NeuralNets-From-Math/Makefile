TEX=main.tex
OUT=release/NeuralNets-From-Math.pdf
# Gather LaTeX sources to trigger rebuilds when chapters or parts change
SOURCES=$(TEX) \
        $(wildcard chapters/*.tex) \
        $(wildcard frontmatter/*.tex) \
        $(wildcard appendices/*.tex) \
        $(wildcard backmatter/*.tex) \
        $(wildcard styles/*.sty)

all: $(OUT)
pdf: $(OUT)

$(OUT): $(SOURCES)
	mkdir -p release
	latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=release main.tex
	@if [ -f release/main.pdf ]; then mv release/main.pdf $(OUT); fi

clean:
	latexmk -C -output-directory=release
	rm -f $(OUT)

view: pdf
	open $(OUT)

help:
	@echo "Available targets:"
	@echo "  make pdf    - Build the PDF from LaTeX sources"
	@echo "  make view   - Build and open the PDF in the default viewer"
	@echo "  make clean  - Remove build artifacts and the generated PDF"
	@echo "  make help   - Show this help message"

.PHONY: all clean pdf view help



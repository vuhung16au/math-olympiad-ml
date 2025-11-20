TEXFILE = RationalEverywhereNowhere
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = release

.PHONY: all pdf clean release open

all: pdf

pdf: $(PDFFILE)

$(PDFFILE): $(TEXFILE).tex $(wildcard sections/*.tex) $(wildcard styles/*.sty)
	pdflatex -interaction=nonstopmode $(TEXFILE).tex || true
	pdflatex -interaction=nonstopmode $(TEXFILE).tex || true
	@if [ ! -f $(PDFFILE) ]; then \
		echo "Error: PDF file was not created!"; \
		exit 1; \
	fi

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).log $(TEXFILE).out $(TEXFILE).toc $(TEXFILE).pdf
	rm -f $(TEXFILE).exa $(TEXFILE).rem $(TEXFILE).tak

release: $(PDFFILE)
	mkdir -p $(RELEASE_DIR)
	cp $(PDFFILE) $(RELEASE_DIR)/

open: $(PDFFILE)
	@if command -v open > /dev/null; then \
		open $(PDFFILE); \
	elif command -v xdg-open > /dev/null; then \
		xdg-open $(PDFFILE); \
	elif command -v start > /dev/null; then \
		start $(PDFFILE); \
	else \
		echo "Error: No PDF viewer command found. Please open $(PDFFILE) manually."; \
		exit 1; \
	fi


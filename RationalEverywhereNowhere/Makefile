TEXFILE = RationalEverywhereNowhere
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = release

.PHONY: all pdf clean release

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


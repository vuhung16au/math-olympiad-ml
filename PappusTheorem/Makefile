TEXFILE = PappusTheorem
PDFFILE = $(TEXFILE).pdf
RELEASE_DIR = releases

.PHONY: all pdf clean release

all: pdf

pdf: $(PDFFILE)

$(PDFFILE): $(TEXFILE).tex
	docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
		pdflatex -interaction=nonstopmode $(TEXFILE).tex
	docker run --rm -v "$(CURDIR):/workdir" -w /workdir texlive/texlive:latest \
		pdflatex -interaction=nonstopmode $(TEXFILE).tex

clean:
	rm -f $(TEXFILE).aux $(TEXFILE).log $(TEXFILE).out $(TEXFILE).toc $(TEXFILE).pdf

release: $(PDFFILE)
	mkdir -p $(RELEASE_DIR)
	cp $(PDFFILE) $(RELEASE_DIR)/


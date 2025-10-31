# Simple Makefile to build the LaTeX document

TEX= T6-219-The-Problem.tex
PDF= T6-219-The-Problem.pdf

LATEX= xelatex
LATEXFLAGS= -interaction=nonstopmode -halt-on-error

.PHONY: pdf clean view release

pdf: clean $(PDF)

$(PDF): $(TEX)
	$(LATEX) $(LATEXFLAGS) $(TEX)
	$(LATEX) $(LATEXFLAGS) $(TEX)

view: $(PDF)
	open $(PDF)

clean:
	rm -f $(PDF) *.aux *.log *.out *.toc *.synctex.gz *.nav *.snm *.fls *.fdb_latexmk

release: $(PDF)
	mkdir -p pdfs
	cp $(PDF) pdfs/$(PDF)

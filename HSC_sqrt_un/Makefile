# Makefile for HSC-Maths-Un-Sequence-Proof.tex

TEX_FILE = HSC-Maths-Un-Sequence-Proof.tex
PDF_FILE = HSC-Maths-Un-Sequence-Proof.pdf
RELEASE_DIR = release

.PHONY: pdf clean release view

pdf: $(PDF_FILE)

$(PDF_FILE): $(TEX_FILE)
	pdflatex $(TEX_FILE)
	pdflatex $(TEX_FILE)

clean:
	rm -f $(PDF_FILE)
	rm -f *.aux *.log *.out *.toc *.synctex.gz

release: clean pdf
	mkdir -p $(RELEASE_DIR)
	cp $(PDF_FILE) $(RELEASE_DIR)/

view: $(PDF_FILE)
	open $(PDF_FILE)


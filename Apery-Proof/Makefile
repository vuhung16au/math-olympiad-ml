# Makefile for Proof-Euler-Missed.tex

TEX_FILE = Proof-Euler-Missed.tex
PDF_FILE = Proof-Euler-Missed.pdf
BASE_NAME = $(basename $(TEX_FILE))

# Default target: compile PDF
.PHONY: default pdf open clean release

default: pdf

pdf: $(PDF_FILE)

$(PDF_FILE): $(TEX_FILE)
	pdflatex -interaction=nonstopmode $(TEX_FILE)
	pdflatex -interaction=nonstopmode $(TEX_FILE)

open: $(PDF_FILE)
	@(command -v xdg-open > /dev/null 2>&1 && xdg-open $(PDF_FILE)) || (command -v evince > /dev/null 2>&1 && evince $(PDF_FILE) &) || (command -v okular > /dev/null 2>&1 && okular $(PDF_FILE) &) || echo "No PDF viewer found. Please open $(PDF_FILE) manually."

clean:
	rm -f $(BASE_NAME).aux $(BASE_NAME).log $(BASE_NAME).out $(BASE_NAME).toc $(BASE_NAME).pdf

release: $(PDF_FILE)
	@mkdir -p releases
	@cp $(PDF_FILE) releases/
	@echo "Released $(PDF_FILE) to releases/"

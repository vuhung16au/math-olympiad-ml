# Makefile for HSC Differential Equations Project

PROJECT = HSC-DifferentialEquations
TEX = pdflatex
LATEXMK = latexmk

$(shell mkdir -p releases samples)

all: pdf

pdf:
	$(LATEXMK) -pdf $(PROJECT).tex

clean:
	$(LATEXMK) -C $(PROJECT).tex
	rm -f *.aux *.log *.toc *.out *.fls *.fdb_latexmk

release: pdf
	mkdir -p releases
	cp $(PROJECT).pdf releases/$(PROJECT).pdf

open:
	open $(PROJECT).pdf

.PHONY: all pdf clean release open

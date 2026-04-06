# Makefile for HSC Trigonometry Project

# Include common variables if available
# -include ../common/Makefile.inc

# Project configuration
PROJECT = HSC-Trigonometry
TEX = pdflatex
LATEXMK = latexmk

# Ensure directories exist
$(shell mkdir -p releases samples)

# Default target
all: pdf

# Compile PDF using latexmk for multiple passes
pdf:
	$(LATEXMK) -pdf $(PROJECT).tex

# Clean auxiliary files
clean:
	$(LATEXMK) -C $(PROJECT).tex
	rm -f *.aux *.log *.toc *.out *.fls *.fdb_latexmk

release:
	$(LATEXMK) -pdf $(PROJECT).tex
	cp $(PROJECT).pdf releases/

open:
	open $(PROJECT).pdf

.PHONY: all pdf clean release open

# Makefile for HSC Functions Project

# Include common variables if available
# -include ../common/Makefile.inc

# Project configuration
PROJECT = HSC-Functions
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

release: pdf
	mkdir -p releases
	cp $(PROJECT).pdf releases/$(PROJECT).pdf

open:
	open $(PROJECT).pdf

.PHONY: all pdf clean release open

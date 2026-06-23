# Makefile for HSC Differential Equations Project

PROJECT = HSC-DifferentialEquations

$(shell mkdir -p releases samples)

all: pdf

pdf:
	@if command -v latexmk >/dev/null 2>&1; then \
		latexmk -pdf -interaction=nonstopmode -file-line-error $(PROJECT).tex; \
	else \
		docker run --rm -v "$(CURDIR)/..:/workspace" -w /workspace/HSC-DifferentialEquations texlive/texlive:latest \
			latexmk -pdf -interaction=nonstopmode -file-line-error $(PROJECT).tex; \
	fi

clean:
	rm -f $(PROJECT).aux $(PROJECT).log $(PROJECT).out $(PROJECT).toc $(PROJECT).pdf \
		$(PROJECT).fdb_latexmk $(PROJECT).fls

release: pdf
	mkdir -p releases
	cp $(PROJECT).pdf releases/$(PROJECT).pdf

open:
	open $(PROJECT).pdf

.PHONY: all pdf clean release open

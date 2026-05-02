# Orchestration Makefile for building all HSC-* LaTeX booklets and HSC-Viewer.
# Run from repo root: make -C HSC-Common <target>

SCRIPTS_DIR := $(CURDIR)/scripts

.PHONY: help build-all clean-all pdf-all release-all

help:
	@echo "HSC-Common orchestration — run from repo root:"
	@echo "  make -C HSC-Common help"
	@echo ""
	@echo "Targets:"
	@echo "  build-all    - Full rebuild each project: LaTeX booklets use"
	@echo "                 'make clean && make pdf'; HSC-Viewer uses"
	@echo "                 'make clean && make build'."
	@echo "  clean-all    - Run make clean in every listed HSC-* directory."
	@echo "  pdf-all      - Run make pdf for LaTeX booklets (skips HSC-Viewer)."
	@echo "  release-all  - Run make release where defined (skips HSC-Viewer)."
	@echo ""
	@echo "Scripts live in: $(SCRIPTS_DIR)"

build-all:
	@$(SCRIPTS_DIR)/build-all-hsc.sh

clean-all:
	@$(SCRIPTS_DIR)/clean-all-hsc.sh

pdf-all:
	@$(SCRIPTS_DIR)/pdf-all-hsc.sh

release-all:
	@$(SCRIPTS_DIR)/release-all-hsc.sh

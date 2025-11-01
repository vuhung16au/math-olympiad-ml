LATEX = pdflatex
MAIN = StrangeNestSquareRoots
RELEASE_DIR = release

.PHONY: all pdf release view clean simul density-simulate

all: pdf

pdf: $(MAIN).pdf

release: $(MAIN).pdf
	@mkdir -p $(RELEASE_DIR)
	cp $(MAIN).pdf $(RELEASE_DIR)/$(MAIN).pdf

view: $(MAIN).pdf
	open $(MAIN).pdf

clean:
	rm -f $(MAIN).pdf
	rm -f $(MAIN).aux $(MAIN).log $(MAIN).out $(MAIN).synctex.gz
	rm -f $(MAIN).toc $(MAIN).lof $(MAIN).lot $(MAIN).fls $(MAIN).fdb_latexmk

$(MAIN).pdf: $(MAIN).tex
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex

# Check if .md file exists and regenerate .tex if needed
$(MAIN).tex: 
	@if [ -f $(MAIN).md ]; then \
		echo "Generating $(MAIN).tex from $(MAIN).md..."; \
		if command -v pandoc >/dev/null 2>&1; then \
			pandoc $(MAIN).md -o $(MAIN).tex; \
		else \
			echo "Warning: pandoc not found. Using existing $(MAIN).tex if available."; \
			if [ ! -f $(MAIN).tex ]; then \
				echo "Error: $(MAIN).tex does not exist and pandoc is not available."; \
				exit 1; \
			fi; \
		fi; \
	elif [ -f $(MAIN).tex ]; then \
		echo "Using existing $(MAIN).tex (no $(MAIN).md found)."; \
	else \
		echo "Error: Neither $(MAIN).md nor $(MAIN).tex exists."; \
		exit 1; \
	fi

# Optional dependency: regenerate tex if md is newer
ifneq ($(wildcard $(MAIN).md),)
$(MAIN).tex: $(MAIN).md
endif

# Simulation targets
simul: density-simulate

density-simulate:
	@echo "Running density simulation..."
	@if [ -d .venv ]; then \
		echo "Activating virtual environment and running simulation..."; \
		.venv/bin/python StrangeNestSquareRoots.py; \
	else \
		echo "Warning: Virtual environment .venv not found."; \
		echo "Attempting to run with system Python..."; \
		python3 StrangeNestSquareRoots.py || python StrangeNestSquareRoots.py; \
	fi
	@echo "Simulation complete. Check ./data/ for output files."

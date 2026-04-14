WIDTH ?= 1280
HEIGHT ?= 720

.PHONY: help fractals

help: ## Show available targets
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

fractals: ## Build and generate all fractal artifacts into artifacts/
	npm run build
	node scripts/generate-all-fractals.js --width $(WIDTH) --height $(HEIGHT)

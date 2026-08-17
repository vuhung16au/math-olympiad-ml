# Delegate HSC booklet orchestration to HSC-Common (see HSC-Common/Makefile).

.PHONY: help build-all clean-all pdf-all release-all clean

help build-all clean-all pdf-all release-all:
	@$(MAKE) -C HSC-Common $@

clean:
	@echo "Cleaning build artifacts, node_modules, python venvs, and caches..."
	find . -type d -name "node_modules" -prune -exec rm -rf {} +
	find . -type d -name "venv" -prune -exec rm -rf {} +
	find . -type d -name ".venv" -prune -exec rm -rf {} +
	find . -type d -name "env" -prune -exec rm -rf {} +
	find . -type d -name ".env" -prune -exec rm -rf {} +
	find . -type d -name "build" -prune -exec rm -rf {} +
	find . -type d -name "dist" -prune -exec rm -rf {} +
	find . -type d -name ".cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	@echo "Clean complete."

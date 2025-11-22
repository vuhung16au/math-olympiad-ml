.PHONY: venv setup drone-show drone-show-production export-paths test clean-drone clean-venv clean-all

# Create virtual environment using uv
venv:
	@echo "Creating virtual environment..."
	uv venv .venv
	@echo "Virtual environment created at .venv"
	@echo "Activate with: source .venv/bin/activate"

# Setup: create venv and install dependencies
setup: venv
	@echo "Installing dependencies..."
	uv pip install -r requirements.txt
	@echo "✓ Setup complete!"

# Run drone show in testing mode (16 seconds)
drone-show:
	@echo "Running drone show (testing mode)..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python drone_show.py --mode testing --output outputs/drone_show_testing.mp4; \
	else \
		python drone_show.py --mode testing --output outputs/drone_show_testing.mp4; \
	fi

# Run drone show in production mode (120 seconds)
drone-show-production:
	@echo "Running drone show (production mode)..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python drone_show.py --mode production --output outputs/drone_show_production.mp4; \
	else \
		python drone_show.py --mode production --output outputs/drone_show_production.mp4; \
	fi

# Export flight paths for real-world operations
export-paths:
	@echo "Exporting flight paths..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python drone_show.py --mode testing --export-paths --output outputs/drone_show_export.mp4; \
	else \
		python drone_show.py --mode testing --export-paths --output outputs/drone_show_export.mp4; \
	fi

# Run tests
test:
	@echo "Running tests..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python -m pytest tests/ -v; \
	else \
		python -m pytest tests/ -v; \
	fi

# Clean drone show outputs
clean-drone:
	@echo "Cleaning drone show outputs..."
	@find outputs/ -type f -name "drone_show*.mp4" -delete 2>/dev/null || true
	@find outputs/ -type f -name "drone_show*.json" -delete 2>/dev/null || true
	@find outputs/ -type f -name "drone_show*.csv" -delete 2>/dev/null || true
	@find outputs/ -type f -name "drone_show*.txt" -delete 2>/dev/null || true
	@echo "Drone show outputs cleaned."

# Remove virtual environment
clean-venv:
	@echo "Removing virtual environment..."
	@rm -rf .venv
	@echo "Virtual environment removed."

# Clean everything
clean-all: clean-drone
	@echo "Cleaning Python cache..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "All cleaned."


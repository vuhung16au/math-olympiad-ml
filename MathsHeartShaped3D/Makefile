.PHONY: clean-inputs clean-outputs clean-all

# Delete all .mp3, .mp4, and .json files in inputs/
clean-inputs:
	@echo "Cleaning input files..."
	@find inputs/ -type f \( -name "*.mp3" -o -name "*.mp4" -o -name "*.json" \) -delete
	@echo "Input files cleaned."

# Delete all .mp4 files in outputs/
clean-outputs:
	@echo "Cleaning output files..."
	@find outputs/ -type f -name "*.mp4" -delete
	@echo "Output files cleaned."

# Clean both inputs and outputs
clean-all: clean-inputs clean-outputs
	@echo "All files cleaned."


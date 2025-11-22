#!/bin/bash
# Export flight paths for real-world operations

set -e

echo "=========================================="
echo "Drone Show - Export Flight Paths"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run drone show with path export
python drone_show.py --mode testing --export-paths --output outputs/drone_show_export.mp4

echo ""
echo "✓ Path export complete!"
echo "  Video: outputs/drone_show_export.mp4"
echo "  Paths: outputs/drone_show_export_paths.json"
echo "  Paths: outputs/drone_show_export_paths.csv"
echo "  Validation: outputs/drone_show_export_paths_validation.txt"
echo ""


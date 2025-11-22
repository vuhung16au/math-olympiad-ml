#!/bin/bash
# Run drone show in testing mode (16 seconds, 2s per scene)

set -e

echo "=========================================="
echo "Drone Show - Testing Mode"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run drone show
python drone_show.py --mode testing --output outputs/drone_show_testing.mp4

echo ""
echo "✓ Testing render complete!"
echo "  Output: outputs/drone_show_testing.mp4"
echo ""


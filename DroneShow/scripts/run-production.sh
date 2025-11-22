#!/bin/bash
# Run drone show in production mode (120 seconds, 15s per scene)

set -e

echo "=========================================="
echo "Drone Show - Production Mode"
echo "=========================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run drone show
python drone_show.py --mode production --output outputs/drone_show_production.mp4

echo ""
echo "✓ Production render complete!"
echo "  Output: outputs/drone_show_production.mp4"
echo ""


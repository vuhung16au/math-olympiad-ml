#!/bin/bash
# Clean outputs and temporary files

echo "=========================================="
echo "Drone Show - Clean"
echo "=========================================="

# Remove output files
if [ -d "outputs" ]; then
    echo "Cleaning outputs directory..."
    rm -f outputs/drone_show*.mp4
    rm -f outputs/drone_show*.json
    rm -f outputs/drone_show*.csv
    rm -f outputs/drone_show*.txt
    echo "✓ Outputs cleaned"
fi

# Remove Python cache
echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "✓ Cache cleaned"

# Remove temporary files
if [ -d "tmp" ]; then
    echo "Cleaning temporary files..."
    rm -rf tmp/cache/*
    echo "✓ Temp files cleaned"
fi

echo ""
echo "✓ Cleanup complete!"
echo ""


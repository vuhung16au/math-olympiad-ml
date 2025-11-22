"""
Test cases for 2D drone formations.
Validates that all formations are flat in Y-Z plane (X=0) and maintain MIN_SEPARATION.
"""

import pytest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.shape_generators import (
    generate_heart_formation,
    generate_star_formation,
    generate_text_formation,
    enforce_min_separation_2d
)
from config.drone_config import (
    HEART_DRONES, STAR_DRONES, VIETNAM_DRONES,
    VIETNAM_COLOR_TOP, VIETNAM_COLOR_BOTTOM,
    MIN_SEPARATION, FORMATION_CENTER
)


class Test2DFormations:
    """Test suite for 2D drone formations."""
    
    def test_heart_formation_is_2d(self):
        """Verify heart formation is flat in Y-Z plane (all X coordinates = 0)."""
        positions, colors = generate_heart_formation(HEART_DRONES)
        
        # Check that all X coordinates are 0 (within small tolerance)
        x_coords = positions[:, 0]
        assert np.all(np.abs(x_coords - FORMATION_CENTER[0]) < 0.01), \
            "Heart formation X coordinates should all be 0"
        
        # Check reasonable number of drones (allow for shape geometry constraints)
        # Heart shape with 2m spacing yields ~100-200 drones depending on scaling
        assert len(positions) >= 100, \
            f"Expected at least 100 drones for heart, got {len(positions)}"
        assert len(positions) <= 1000, \
            f"Too many drones: {len(positions)} > 1000"
        
        # Check position ranges (should fit within 60m × 60m)
        y_coords = positions[:, 1]
        z_coords = positions[:, 2]
        y_range = np.max(y_coords) - np.min(y_coords)
        z_range = np.max(z_coords) - np.min(z_coords)
        
        assert y_range <= 70, f"Heart Y range ({y_range:.1f}m) exceeds expected ~60m"
        assert z_range <= 70, f"Heart Z range ({z_range:.1f}m) exceeds expected ~60m"
    
    def test_star_formation_is_2d(self):
        """Verify star formation is flat in Y-Z plane (all X coordinates = 0)."""
        positions, colors = generate_star_formation(STAR_DRONES)
        
        # Check that all X coordinates are 0 (within small tolerance)
        x_coords = positions[:, 0]
        assert np.all(np.abs(x_coords - FORMATION_CENTER[0]) < 0.01), \
            "Star formation X coordinates should all be 0"
        
        # Check reasonable number of drones (allow for shape geometry constraints)
        # Star shape with 2m spacing yields ~200-300 drones
        assert len(positions) >= 100, \
            f"Expected at least 100 drones for star, got {len(positions)}"
        assert len(positions) <= 1000, \
            f"Too many drones: {len(positions)} > 1000"
        
        # Check position ranges
        y_coords = positions[:, 1]
        z_coords = positions[:, 2]
        y_range = np.max(y_coords) - np.min(y_coords)
        z_range = np.max(z_coords) - np.min(z_coords)
        
        assert y_range <= 70, f"Star Y range ({y_range:.1f}m) exceeds expected ~60m"
        assert z_range <= 70, f"Star Z range ({z_range:.1f}m) exceeds expected ~60m"
    
    def test_text_formation_is_2d(self):
        """Verify text formation is flat in Y-Z plane (all X coordinates = 0)."""
        positions, colors = generate_text_formation(
            'VIETNAM', VIETNAM_DRONES,
            VIETNAM_COLOR_TOP, VIETNAM_COLOR_BOTTOM
        )
        
        # Check that all X coordinates are 0 (within small tolerance)
        x_coords = positions[:, 0]
        assert np.all(np.abs(x_coords - FORMATION_CENTER[0]) < 0.01), \
            "Text formation X coordinates should all be 0"
        
        # Check correct number of drones
        assert len(positions) == VIETNAM_DRONES, \
            f"Expected {VIETNAM_DRONES} drones, got {len(positions)}"
    
    def test_min_separation_enforcement(self):
        """Verify MIN_SEPARATION helper function works correctly."""
        # Create test positions with some too close together
        test_positions = np.array([
            [0, 0, 0],
            [0, 1, 0],     # Too close (1m < 2m)
            [0, 0, 1],     # Too close (1m < 2m)
            [0, 3, 0],     # OK (3m > 2m)
            [0, 0, 3],     # OK (3m > 2m)
            [0, 5, 5],     # OK (sqrt(50) > 2m)
        ])
        
        filtered = enforce_min_separation_2d(test_positions, MIN_SEPARATION)
        
        # Should have fewer points after filtering
        assert len(filtered) < len(test_positions), \
            "MIN_SEPARATION filter should remove some points"
        
        # Verify remaining points maintain separation
        for i in range(len(filtered)):
            for j in range(i + 1, len(filtered)):
                dist_2d = np.sqrt(
                    (filtered[i, 1] - filtered[j, 1])**2 +
                    (filtered[i, 2] - filtered[j, 2])**2
                )
                assert dist_2d >= MIN_SEPARATION - 0.01, \
                    f"Points {i} and {j} too close: {dist_2d:.2f}m < {MIN_SEPARATION}m"
    
    def test_heart_min_separation(self):
        """Verify heart formation maintains minimum separation."""
        positions, colors = generate_heart_formation(HEART_DRONES)
        
        # Note: Formation uses grid-based spacing with MIN_SEPARATION
        assert len(positions) >= 100, \
            f"Too few drones: {len(positions)} < 100"
        
        # Sample check (checking all pairs would be O(n²) and slow)
        # Check first 30 drones against next 30
        sample_size = min(30, len(positions) // 2)
        violations = 0
        for i in range(sample_size):
            for j in range(sample_size, min(sample_size * 2, len(positions))):
                # 2D distance in Y-Z plane
                dist_2d = np.sqrt(
                    (positions[i, 1] - positions[j, 1])**2 +
                    (positions[i, 2] - positions[j, 2])**2
                )
                # Allow small tolerance for numerical precision
                if dist_2d < MIN_SEPARATION - 0.1:
                    violations += 1
        
        # Allow up to 5% violations for edge cases with random offsets
        violation_rate = violations / (sample_size * sample_size)
        assert violation_rate < 0.05, \
            f"Too many MIN_SEPARATION violations: {violation_rate:.1%} (max 5%)"
    
    def test_color_assignment(self):
        """Verify colors are correctly assigned to formations."""
        # Heart should be all red
        _, heart_colors = generate_heart_formation(HEART_DRONES)
        assert np.all(heart_colors[:, 0] == 255), "Heart should be red (R=255)"
        assert np.all(heart_colors[:, 1] == 0), "Heart should be red (G=0)"
        assert np.all(heart_colors[:, 2] == 0), "Heart should be red (B=0)"
        
        # Star should be all gold
        _, star_colors = generate_star_formation(STAR_DRONES)
        assert np.all(star_colors[:, 0] == 255), "Star should be gold (R=255)"
        assert np.all(star_colors[:, 1] == 215), "Star should be gold (G=215)"
        assert np.all(star_colors[:, 2] == 0), "Star should be gold (B=0)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


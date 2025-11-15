"""
Pytest test cases for heart_animation.py
"""

import pytest
import os
import sys
import subprocess
import tempfile
import shutil

# Add parent directory to path to import heart_animation
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from heart_animation import create_animation


class TestHeartAnimation:
    """Test cases for heart animation generation."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary directory for test outputs."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup: remove temporary directory after test
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    
    def test_case_1_effect_a_small_resolution(self, temp_output_dir):
        """
        Test Case 1: Simple test with Effect A, small resolution, low bitrate.
        
        This is the first and simplest test case to verify basic functionality:
        - Effect: A (Multi-axis rotation)
        - Resolution: small (640x480)
        - Bitrate: 2000 kbps
        """
        output_path = os.path.join(temp_output_dir, "test_effect_a_small.mp4")
        
        # Run animation generation
        create_animation(
            resolution='small',
            dpi=100,
            density='lower',  # Use lower density for faster testing
            effect='A',
            show_axes=False,
            show_formulas=False,
            fps=30,
            bitrate=2000,
            output_path=output_path,
            watermark='',  # No watermark for testing
            audio_features_path=None
        )
        
        # Verify output file was created
        assert os.path.exists(output_path), f"Output file not created: {output_path}"
        
        # Verify file is not empty (has some content)
        file_size = os.path.getsize(output_path)
        assert file_size > 0, f"Output file is empty: {output_path}"
        
        # Basic sanity check: file should be at least a few KB for a video
        # (even a very short video should be > 1KB)
        assert file_size > 1024, f"Output file too small ({file_size} bytes), may be corrupted"
        
        print(f"Test passed: Generated {output_path} ({file_size} bytes)")
    
    @pytest.mark.skip(reason="Not yet implemented - Test Case 2: Resolution tests")
    def test_case_2_resolution_tests(self, temp_output_dir):
        """
        Test Case 2: Resolution tests.
        
        Test all resolution options:
        - small (640x480)
        - medium (1280x720)
        - large (1920x1080)
        - 4k (3840x2160)
        
        Verify that each resolution produces valid output files.
        """
        # TODO: Implement resolution tests
        # For each resolution:
        #   1. Generate animation with that resolution
        #   2. Verify output file exists and is valid
        #   3. Optionally verify dimensions match expected resolution
        pass
    
    @pytest.mark.skip(reason="Not yet implemented - Test Case 3: Effect tests")
    def test_case_3_effect_tests(self, temp_output_dir):
        """
        Test Case 3: Effect tests.
        
        Test all available effects:
        - Basic effects: A, B, C, D, E, F, G
        - Epic effects: G1, G2
        - H series: H1, H2, H3, H4, H5, H6, H7, H8, H8sync
        
        Verify that each effect:
        1. Can be instantiated
        2. Generates valid output
        3. Produces expected frame count
        4. (Optional) Matches expected visual characteristics
        """
        # TODO: Implement effect tests
        # For each effect:
        #   1. Generate animation with that effect
        #   2. Verify output file exists and is valid
        #   3. Verify total frames match expected duration
        #   4. For H8sync, test with and without audio features
        pass


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])


# Unit Testing for Heart Animation

## Overview

This document describes the unit testing strategy for the heart animation generator. The test suite uses `pytest` to verify that the animation generation works correctly across different configurations, effects, and resolutions.

The testing approach focuses on:
- **Functional correctness**: Ensuring animations are generated successfully
- **Output validation**: Verifying output files are created and valid
- **Configuration coverage**: Testing different combinations of parameters
- **Effect coverage**: Ensuring all 18 effects work correctly

## Purpose of Testing

### Primary Goals

1. **Regression Prevention**: Catch bugs introduced by code changes
2. **Functionality Verification**: Ensure all features work as expected
3. **Quality Assurance**: Validate output files are properly generated
4. **Documentation**: Tests serve as executable documentation of expected behavior

### Testing Scope

The test suite covers:
- ✅ Basic animation generation (Test Case 1)
- ⏳ Resolution options (Test Case 2 - planned)
- ⏳ All 18 effects (Test Case 3 - planned)
- ⏳ Audio synchronization (future)
- ⏳ Edge cases and error handling (future)

## Test Cases

### Test Case 1: Simple Basic Test ✅

**Status**: Implemented

**Purpose**: Verify basic functionality with the simplest configuration.

**Configuration**:
- Effect: `A` (Multi-axis rotation)
- Resolution: `small` (640x480)
- Bitrate: `2000` kbps
- Density: `lower` (for faster testing)

**Verification**:
- Output file is created
- File is not empty
- File size is reasonable (> 1KB)

**Command equivalent**:
```bash
python heart_animation.py --effect A --resolution small --bitrate 2000 --density lower --output test_output.mp4
```

### Test Case 2: Resolution Tests ⏳

**Status**: Planned (not yet implemented)

**Purpose**: Verify all resolution options produce valid output.

**Test Matrix**:
- `small` (640x480)
- `medium` (1280x720)
- `large` (1920x1080)
- `4k` (3840x2160)

**Verification**:
- Each resolution generates valid output
- Output files are created successfully
- File sizes scale appropriately with resolution
- (Optional) Verify video dimensions match expected resolution

**Implementation Notes**:
- Use same effect (`A`) for consistency
- Use lower density for faster execution
- May need to verify video metadata for actual resolution

### Test Case 3: Effect Tests ⏳

**Status**: Planned (not yet implemented)

**Purpose**: Verify all 18 effects work correctly.

**Effects to Test**:
- **Basic Effects**: A, B, C, D, E, F, G
- **Epic Effects**: G1, G2
- **H Series**: H1, H2, H3, H4, H5, H6, H7, H8, H8sync

**Verification for Each Effect**:
1. Effect can be instantiated without errors
2. Animation generates successfully
3. Output file is valid
4. Total frames match expected duration
5. (For H8sync) Test with and without audio features

**Special Considerations**:
- **H4**: Requires second heart generation
- **H8sync**: Requires audio features JSON file
- **Long effects** (G2: 137s, H4: 120s): May need reduced frame count for testing
- **Different durations**: Verify frame counts match expected durations

**Test Structure**:
```python
@pytest.mark.parametrize("effect,expected_frames", [
    ('A', 900),      # 30 seconds at 30 fps
    ('G1', 2700),    # 90 seconds at 30 fps
    ('H8sync', 3000), # 100 seconds at 30 fps
    # ... etc
])
def test_effect_generation(effect, expected_frames):
    # Test implementation
```

## Running Tests

### Prerequisites

Install pytest:
```bash
pip install pytest
```

### Run All Tests

```bash
# From project root
pytest tests/

# With verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_heart_animation.py::TestHeartAnimation::test_case_1_effect_a_small_resolution -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=heart_animation --cov=core --cov=effects --cov=config
```

## Test Environment

### Temporary Output Directory

Tests use a temporary directory for output files that is automatically cleaned up after each test:

```python
@pytest.fixture
def temp_output_dir(self):
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)  # Cleanup
```

### Test Configuration

For faster test execution:
- Use `lower` density (fewer points)
- Use `small` resolution
- Use lower bitrate (2000 kbps)
- Consider reducing frame count for long effects

## Future Test Cases

### Test Case 4: Audio Synchronization
- Test H8sync with valid audio features
- Test H8sync without audio features (fallback)
- Verify audio feature loading
- Test with invalid/malformed audio features

### Test Case 5: Error Handling
- Invalid effect name
- Invalid resolution
- Invalid density
- Missing output directory permissions
- Invalid audio features file

### Test Case 6: Performance Tests
- Measure generation time for different configurations
- Memory usage tests
- Large resolution performance (4K)

### Test Case 7: Integration Tests
- Full workflow: analyze_audio.py → heart_animation.py
- PowerShell script integration
- Output file format validation

## Test Data

### Sample Audio Features

For testing H8sync, use:
- `H8InfiniteStars2_100s_features.json` (if available)
- Or generate test data with `analyze_audio.py`

### Test Outputs

Test outputs are stored in temporary directories and cleaned up automatically. For manual inspection, tests can be modified to keep outputs:

```python
# Keep output for inspection
output_path = os.path.join(temp_output_dir, "keep_this.mp4")
# ... generate animation ...
# Don't cleanup temp_output_dir
```

## Continuous Integration

### GitHub Actions (Future)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest tests/ --cov
```

## Notes

- **Test Duration**: Some effects (G2: 137s) take significant time to generate. Consider using reduced frame counts or timeouts for CI/CD.
- **FFmpeg Dependency**: Tests require FFmpeg to be installed and available in PATH.
- **Platform Differences**: Video encoding may vary slightly between platforms (Windows/Linux/macOS).
- **File Size Validation**: File sizes may vary based on content, so use reasonable thresholds rather than exact values.

## Contributing

When adding new effects or features:
1. Add corresponding test cases
2. Update this documentation
3. Ensure tests pass before submitting PR
4. Consider edge cases and error scenarios


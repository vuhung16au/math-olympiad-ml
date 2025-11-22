"""
Drone Show Configuration
Contains all constants and parameters for the drone show simulation.
"""

import numpy as np

# ============================================================================
# PERFORMANCE SPACE
# ============================================================================
SPACE_WIDTH = 100.0  # meters
SPACE_DEPTH = 100.0  # meters
SPACE_HEIGHT = 30.0  # meters
FORMATION_CENTER = (0.0, 0.0, 15.0)  # Center point for formations

# ============================================================================
# DRONE SPECIFICATIONS
# ============================================================================
TOTAL_DRONES = 1000
MAX_SPEED = 4.0  # m/s
ACCELERATION = 2.0  # m/s²
DECELERATION = 2.0  # m/s²
MIN_SEPARATION = 2.0  # meters (collision avoidance threshold)
POSITION_DRIFT = 0.1  # meters (random position variation)
DRONE_VISUAL_SIZE = 0.5  # meters (visual representation diameter)

# ============================================================================
# PARKING GRID (for inactive drones)
# ============================================================================
PARKING_Z = 0.0  # Ground level
PARKING_GRID_SIZE = 90.0  # 90m × 90m
PARKING_SPACING = 3.0  # meters between parked drones

# ============================================================================
# CAMERA CONFIGURATION
# ============================================================================
# 2D Fixed Camera Configuration (audience view)
CAMERA_FIXED = True  # True = fixed position, False = orbiting
CAMERA_POSITION = (150.0, 0.0, 15.0)  # Fixed position: 150m in front, center height
CAMERA_TARGET = (0.0, 0.0, 15.0)  # Look-at point (updated to formation center height)

# Legacy orbit settings (used when CAMERA_FIXED = False)
CAMERA_RADIUS = 200.0  # meters from target
CAMERA_ORBIT_PERIOD = 20.0  # seconds for 360° rotation
CAMERA_HEIGHT_MIN = 100.0  # meters
CAMERA_HEIGHT_MAX = 200.0  # meters
CAMERA_FOV = 60.0  # degrees
CAMERA_INITIAL_ANGLE = 0.0  # degrees (0° = East)

# ============================================================================
# SCENE TIMING
# ============================================================================
SCENE_DURATION_TESTING = 2.0  # seconds per scene
SCENE_DURATION_PRODUCTION = 15.0  # seconds per scene
TRANSITION_DURATION = 1.0  # seconds for cross-fade
FPS = 30  # frames per second

# Scene definitions
SCENES = [
    {'name': 'blackout_start', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'heart', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'star', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'vietnam', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'australia', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'i_love_vietnam', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'i_love_australia', 'duration_testing': 2.0, 'duration_production': 15.0},
    {'name': 'blackout_end', 'duration_testing': 2.0, 'duration_production': 15.0},
]

# ============================================================================
# FORMATION SPECIFICATIONS
# ============================================================================

# Heart formation (2D - flat in Y-Z plane)
HEART_DRONES = 900  # Increased for 2D 60m×60m formation
HEART_WIDTH = 60.0  # meters (was 20.0)
HEART_HEIGHT = 60.0  # meters (was 20.0)
HEART_DEPTH = 0.0  # meters (2D = no depth)
HEART_COLOR = (255, 0, 0)  # Red

# Star formation (2D - flat in Y-Z plane)
STAR_DRONES = 850  # Increased for 2D formation
STAR_DIAMETER = 60.0  # meters (was 18.0)
STAR_DEPTH = 0.0  # meters (2D = no depth)
STAR_POINTS = 5
STAR_COLOR = (255, 215, 0)  # Gold (#FFD700)

# Text formations (2D - flat in Y-Z plane)
TEXT_HEIGHT = 12.0  # meters per character (was 8.0, larger for 60m space)
TEXT_SPACING = 1.5  # meters between characters
TEXT_SAMPLE_INTERVAL = 0.15  # meters along outline paths

# Vietnam text
VIETNAM_DRONES = 700  # Increased for larger text
VIETNAM_COLOR_TOP = (255, 255, 0)  # Yellow
VIETNAM_COLOR_BOTTOM = (255, 0, 0)  # Red

# Australia text
AUSTRALIA_DRONES = 750  # Increased for larger text
AUSTRALIA_COLOR_TOP = (0, 128, 0)  # Green
AUSTRALIA_COLOR_BOTTOM = (255, 215, 0)  # Gold

# Combined texts
I_LOVE_VIETNAM_DRONES = 850  # Increased for larger formation
I_LOVE_AUSTRALIA_DRONES = 900  # Increased for larger formation
COMBINED_TEXT_SPACING = 3.0  # meters between elements
HEART_EMOJI_DRONES = 100
WHITE_COLOR = (255, 255, 255)

# ============================================================================
# VIDEO OUTPUT SPECIFICATIONS
# ============================================================================
VIDEO_RESOLUTION = (3840, 2160)  # 4K
VIDEO_FPS = 30
VIDEO_BITRATE = 5000  # kbps
VIDEO_CODEC = 'h264'
BACKGROUND_COLOR = (0, 0, 0)  # Black

# ============================================================================
# PATH EXPORT SPECIFICATIONS
# ============================================================================
EXPORT_TIME_INTERVAL = 0.1  # seconds (100ms intervals)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_total_duration(mode='testing'):
    """Calculate total show duration based on mode."""
    if mode == 'testing':
        return sum(scene['duration_testing'] for scene in SCENES)
    else:
        return sum(scene['duration_production'] for scene in SCENES)


def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_normalized(rgb):
    """Convert RGB (0-255) to normalized (0-1) values."""
    return tuple(c / 255.0 for c in rgb)


def interpolate_color(color1, color2, t):
    """Linear interpolation between two RGB colors.
    
    Args:
        color1: RGB tuple (0-255)
        color2: RGB tuple (0-255)
        t: interpolation factor (0-1)
    
    Returns:
        Interpolated RGB tuple (0-255)
    """
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))


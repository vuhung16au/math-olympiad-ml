"""Flat renderer for Rubik's Cube - unfolded cross view.

This module renders the cube in the standard "unfolded cross" layout.
"""

import pygame
from typing import Tuple
from core.cube_state import CubeState


# Custom color palette
COLORS = {
    # Primary Colors
    'bookpurple': (60, 16, 83),
    'bookred': (242, 18, 12),
    'bookblack': (0, 0, 0),
    'bookwhite': (255, 255, 255),
    # Secondary Colors
    'lawpurple': (181, 24, 37),
    'warmstone': (145, 139, 131),
    'deepcharcoal': (48, 44, 42),
    'softivory': (242, 239, 235),
}

# Rubik's cube color mapping to palette
CUBE_COLORS = {
    'W': COLORS['bookwhite'],      # White
    'Y': COLORS['warmstone'],      # Yellow (using warmstone)
    'R': COLORS['bookred'],        # Red
    'O': COLORS['lawpurple'],      # Orange
    'B': COLORS['bookpurple'],     # Blue
    'G': (100, 150, 100),          # Green (derived, complementary to red)
}


class FlatRenderer:
    """Renders the cube in unfolded cross view."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize renderer with screen dimensions.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.update_layout()
    
    def update_layout(self):
        """Update layout based on current screen size."""
        # Calculate sticker size to fit in screen
        # Layout: 4 columns (back, left, front, right) × 3 rows (top, middle, bottom)
        # Leave space for UI: left side (instructions) ~250px, bottom (log) ~80px, right (buttons) ~150px
        left_margin = 250  # Space for instructions
        right_margin = 150  # Space for buttons
        bottom_margin = 80  # Space for log display
        top_margin = 50
        available_width = self.screen_width - left_margin - right_margin
        available_height = self.screen_height - top_margin - bottom_margin
        
        # Each face is 3x3, layout is 4 columns × 3 rows
        cols = 4
        rows = 3
        
        # Calculate size per sticker
        sticker_width = min(available_width // (cols * 3), available_height // (rows * 3))
        self.sticker_size = max(20, sticker_width)  # Minimum 20 pixels
        
        # Calculate offsets to center (accounting for UI margins)
        total_width = cols * 3 * self.sticker_size
        total_height = rows * 3 * self.sticker_size
        self.offset_x = left_margin + (available_width - total_width) // 2
        self.offset_y = top_margin + (available_height - total_height) // 2
    
    def set_screen_size(self, width: int, height: int):
        """Update screen size and recalculate layout.
        
        Args:
            width: New screen width
            height: New screen height
        """
        self.screen_width = width
        self.screen_height = height
        self.update_layout()
    
    def draw(self, screen: pygame.Surface, cube: CubeState):
        """Draw the cube in unfolded cross view.
        
        Args:
            screen: Pygame surface to draw on
            cube: CubeState to render
        """
        # Map faces to grid positions (x, y) in the unfolded cross
        # Layout:
        #     [top]
        # [back] [left] [front] [right]
        #     [bottom]
        layout = {
            'top': (1, 0),      # Column 1, Row 0
            'left': (0, 1),     # Column 0, Row 1
            'front': (1, 1),   # Column 1, Row 1
            'right': (2, 1),    # Column 2, Row 1
            'back': (3, 1),    # Column 3, Row 1
            'bottom': (1, 2),  # Column 1, Row 2
        }
        
        for face_name, (grid_x, grid_y) in layout.items():
            face = cube.get_face(face_name)
            for row in range(3):
                for col in range(3):
                    color_char = face[row][col]
                    # Handle empty or invalid color characters
                    if not color_char or color_char not in CUBE_COLORS:
                        # Log warning for invalid colors but use a fallback
                        import logging
                        logger = logging.getLogger("rubiks_solver")
                        if color_char:
                            logger.warning(f"Invalid color character '{color_char}' at {face_name}[{row}][{col}]")
                        # Use a default color based on face (fallback)
                        default_colors = {
                            'top': CUBE_COLORS['W'],
                            'bottom': CUBE_COLORS['Y'],
                            'front': CUBE_COLORS['G'],
                            'back': CUBE_COLORS['B'],
                            'left': CUBE_COLORS['O'],
                            'right': CUBE_COLORS['R'],
                        }
                        color = default_colors.get(face_name, COLORS['bookblack'])
                    else:
                        color = CUBE_COLORS[color_char]
                    
                    # Calculate position
                    x = self.offset_x + grid_x * 3 * self.sticker_size + col * self.sticker_size
                    y = self.offset_y + grid_y * 3 * self.sticker_size + row * self.sticker_size
                    
                    # Draw sticker with border
                    rect = pygame.Rect(x, y, self.sticker_size - 2, self.sticker_size - 2)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, COLORS['deepcharcoal'], rect, 1)  # Border

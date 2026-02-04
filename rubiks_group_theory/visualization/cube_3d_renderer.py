"""3D renderer for Rubik's Cube - isometric/perspective visualization.

This module renders the cube in 3D showing only the three visible faces
(front, left, top) like a real Rubik's Cube.
"""

import pygame
import math
from typing import Tuple, List
from core.cube_state import CubeState
from visualization.flat_renderer import COLORS, CUBE_COLORS


class Cube3DRenderer:
    """Renders the cube in 3D using isometric projection."""
    
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
        # Layout: 3D render on the RIGHT side, Graph view on the LEFT side
        # Leave space for buttons (150px from right edge)
        left_margin = 250  # Space for instructions (same as graph renderer uses)
        right_margin = 150  # Space for buttons
        
        # Calculate the split point: graph on left, 3D on right
        split_point = left_margin + (self.screen_width - left_margin - right_margin) // 2
        
        # 3D view uses the right portion (from split_point to screen_width - right_margin)
        cube_left = split_point
        cube_right = self.screen_width - right_margin
        cube_width = cube_right - cube_left
        available_height = self.screen_height - 80  # Account for log area
        
        # Center of the 3D cube (in its right portion)
        self.center_x = cube_left + cube_width // 2
        self.center_y = self.screen_height // 2  # Vertical center
        
        # Cube size (sticker size in screen pixels)
        # Make it fit nicely in the right side space
        self.sticker_size = min(cube_width // 12, available_height // 12, 50)
        
        # Isometric projection angles (adjusted for better view)
        self.angle_x = math.radians(30)  # Rotation around X axis
        self.angle_y = math.radians(-35)  # Rotation around Y axis
    
    def set_screen_size(self, width: int, height: int):
        """Update screen size and recalculate layout.
        
        Args:
            width: New screen width
            height: New screen height
        """
        self.screen_width = width
        self.screen_height = height
        self.update_layout()
    
    def _project_3d_to_2d(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """Project 3D coordinates to 2D screen coordinates using isometric projection.
        
        Args:
            x: X coordinate in 3D space (right)
            y: Y coordinate in 3D space (up)
            z: Z coordinate in 3D space (forward/toward viewer)
        
        Returns:
            (screen_x, screen_y) tuple
        """
        # Isometric projection
        # Rotate around Y axis first, then X axis
        cos_y = math.cos(self.angle_y)
        sin_y = math.sin(self.angle_y)
        cos_x = math.cos(self.angle_x)
        sin_x = math.sin(self.angle_x)
        
        # Apply Y rotation
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        y_rot = y
        
        # Apply X rotation
        y_final = y_rot * cos_x - z_rot * sin_x
        z_final = y_rot * sin_x + z_rot * cos_x
        
        # Project to 2D (orthographic projection)
        screen_x = int(self.center_x + x_rot)
        screen_y = int(self.center_y - y_final)  # Y is inverted in screen coordinates
        
        return screen_x, screen_y
    
    def _draw_sticker(self, screen: pygame.Surface, corners: List[Tuple[int, int]], color: tuple):
        """Draw a single sticker as a filled polygon.
        
        Args:
            screen: Pygame surface to draw on
            corners: List of (x, y) screen coordinates for the 4 corners
            color: RGB color tuple
        """
        # Draw filled polygon
        pygame.draw.polygon(screen, color, corners)
        # Draw black border
        pygame.draw.polygon(screen, COLORS['deepcharcoal'], corners, 2)
    
    def _draw_face_stickers(self, screen: pygame.Surface, face_name: str, face_colors: List[List[str]]):
        """Draw all stickers on a given face.
        
        Args:
            screen: Pygame surface to draw on
            face_name: 'top', 'front', or 'left'
            face_colors: 3x3 array of color characters
        """
        s = self.sticker_size
        gap = s * 0.05  # Small gap between stickers
        
        for row in range(3):
            for col in range(3):
                color_char = face_colors[row][col]
                color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
                
                # Calculate sticker position in 3D
                # Each sticker is a small square on the face
                corners_3d = self._get_sticker_corners_3d(face_name, row, col, s, gap)
                
                # Project to 2D
                corners_2d = [self._project_3d_to_2d(x, y, z) for x, y, z in corners_3d]
                
                # Draw the sticker
                self._draw_sticker(screen, corners_2d, color)
    
    def _get_sticker_corners_3d(self, face_name: str, row: int, col: int, 
                                 sticker_size: float, gap: float) -> List[Tuple[float, float, float]]:
        """Get 3D coordinates of the 4 corners of a sticker.
        
        Args:
            face_name: 'top', 'front', or 'left'
            row: Row index (0-2)
            col: Column index (0-2)
            sticker_size: Size of one sticker
            gap: Gap between stickers
        
        Returns:
            List of 4 (x, y, z) tuples representing corners
        """
        s = sticker_size
        g = gap
        
        # Calculate position within the face
        # Face is 3x3 stickers, centered at origin
        # Map col/row to position
        x_offset = (col - 1) * s  # -s, 0, s
        y_offset = (1 - row) * s  # s, 0, -s (invert row for top-to-bottom)
        
        # Sticker corners (local to face, before positioning)
        half = (s - g) / 2
        local_corners = [
            (x_offset - half, y_offset + half),  # Top-left
            (x_offset + half, y_offset + half),  # Top-right
            (x_offset + half, y_offset - half),  # Bottom-right
            (x_offset - half, y_offset - half),  # Bottom-left
        ]
        
        # Position the cube so that its center is at origin
        # Each face is at distance 1.5*s from center
        face_offset = 1.5 * s
        
        corners_3d = []
        if face_name == 'front':
            # Front face: z = +face_offset, x varies, y varies
            for lx, ly in local_corners:
                corners_3d.append((lx, ly, face_offset))
        elif face_name == 'left':
            # Left face: x = -face_offset, y varies, z varies
            # Flip local x so face orientation stays consistent.
            for lx, ly in local_corners:
                corners_3d.append((-face_offset, ly, -lx))
        elif face_name == 'top':
            # Top face: y = +face_offset, x varies, z varies
            # Top face should show stickers facing up with correct orientation
            for lx, ly in local_corners:
                corners_3d.append((lx, face_offset, ly))
        
        return corners_3d
    
    def draw(self, screen: pygame.Surface, cube: CubeState):
        """Draw the cube in 3D showing only the three visible faces.
        
        Args:
            screen: Pygame surface to draw on
            cube: CubeState to render
        """
        # In standard orientation, we show:
        # - Front face (green)
        # - Left face (orange in solved state)
        # - Top face (white)
        
        # Draw in back-to-front order for proper layering
        # Order: top, left, front (front is closest to viewer)
        
        # 1. Draw top face
        top_face = cube.get_face('top')
        self._draw_face_stickers(screen, 'top', top_face)
        
        # 2. Draw left face
        left_face = cube.get_face('left')
        self._draw_face_stickers(screen, 'left', left_face)
        
        # 3. Draw front face
        front_face = cube.get_face('front')
        self._draw_face_stickers(screen, 'front', front_face)

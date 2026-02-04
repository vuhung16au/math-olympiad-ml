"""3D renderer for Rubik's Cube - isometric/perspective visualization.

This module renders the cube in 3D using isometric projection.
"""

import pygame
import math
from typing import Tuple
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
        
        # Cube size (in 3D units, before projection)
        # Make it fit nicely in the right side space
        self.cube_size = min(cube_width // 2, available_height // 3)
        
        # Isometric projection angles
        self.angle_x = math.radians(30)  # Rotation around X axis
        self.angle_y = math.radians(45)  # Rotation around Y axis
    
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
            x: X coordinate in 3D space
            y: Y coordinate in 3D space (up)
            z: Z coordinate in 3D space (depth)
        
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
    
    def _get_face_vertices(self, face_name: str) -> list:
        """Get 3D vertices for a cube face.
        
        Args:
            face_name: One of 'top', 'bottom', 'front', 'back', 'left', 'right'
        
        Returns:
            List of 4 (x, y, z) tuples representing face corners
        """
        s = self.cube_size / 2  # Half cube size
        
        # Define cube vertices in 3D space
        # Cube centered at origin, with size from -s to +s
        faces_3d = {
            'front': [  # Z = +s
                (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)
            ],
            'back': [  # Z = -s
                (s, -s, -s), (-s, -s, -s), (-s, s, -s), (s, s, -s)
            ],
            'right': [  # X = +s
                (s, -s, s), (s, -s, -s), (s, s, -s), (s, s, s)
            ],
            'left': [  # X = -s
                (-s, -s, -s), (-s, -s, s), (-s, s, s), (-s, s, -s)
            ],
            'top': [  # Y = +s
                (-s, s, s), (s, s, s), (s, s, -s), (-s, s, -s)
            ],
            'bottom': [  # Y = -s
                (-s, -s, -s), (s, -s, -s), (s, -s, s), (-s, -s, s)
            ],
        }
        
        return faces_3d.get(face_name, [])
    
    def _get_sticker_3d_pos(self, face_name: str, row: int, col: int) -> Tuple[float, float, float]:
        """Get 3D position of a sticker within a face.
        
        Args:
            face_name: Face name
            row: Row within face (0-2)
            col: Column within face (0-2)
        
        Returns:
            (x, y, z) tuple in 3D space
        """
        s = self.cube_size / 2
        sticker_size = self.cube_size / 3
        # Position within face (from -s+sticker_size/2 to s-sticker_size/2)
        # Map col (0-2) to position (-1, 0, 1) in normalized coordinates
        local_x_norm = (col - 1) * (2/3)  # -2/3, 0, 2/3
        local_y_norm = (1 - row) * (2/3)  # 2/3, 0, -2/3 (invert row)
        
        # Scale to actual size
        local_x = local_x_norm * s
        local_y = local_y_norm * s
        
        # Map to actual 3D position based on face
        # Cube faces are at positions: x=±s, y=±s, z=±s
        if face_name == 'front':  # z = +s
            return (local_x, local_y, s)
        elif face_name == 'back':  # z = -s
            return (-local_x, local_y, -s)
        elif face_name == 'right':  # x = +s
            return (s, local_y, -local_x)
        elif face_name == 'left':  # x = -s
            return (-s, local_y, local_x)
        elif face_name == 'top':  # y = +s
            return (local_x, s, -local_y)
        elif face_name == 'bottom':  # y = -s
            return (local_x, -s, local_y)
        
        return (0, 0, 0)
    
    def draw(self, screen: pygame.Surface, cube: CubeState):
        """Draw the cube in 3D.
        
        Args:
            screen: Pygame surface to draw on
            cube: CubeState to render
        """
        # Draw faces in back-to-front order for proper depth
        # Order: back, left, bottom, right, top, front
        face_order = ['back', 'left', 'bottom', 'right', 'top', 'front']
        
        for face_name in face_order:
            # Draw stickers on this face
            face = cube.get_face(face_name)
            for row in range(3):
                for col in range(3):
                    color_char = face[row][col]
                    color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
                    
                    # Get 3D position and project to 2D
                    x, y, z = self._get_sticker_3d_pos(face_name, row, col)
                    screen_x, screen_y = self._project_3d_to_2d(x, y, z)
                    
                    # Calculate sticker size in screen space
                    sticker_size_3d = self.cube_size / 3
                    # Project a point slightly offset to estimate screen size
                    offset = sticker_size_3d * 0.4
                    x2, y2, z2 = x + offset, y, z
                    screen_x2, screen_y2 = self._project_3d_to_2d(x2, y2, z2)
                    screen_sticker_size = max(6, int(math.sqrt((screen_x2 - screen_x)**2 + (screen_y2 - screen_y)**2)))
                    
                    # Draw sticker as a small square (more visible than circle)
                    sticker_rect = pygame.Rect(
                        screen_x - screen_sticker_size // 2,
                        screen_y - screen_sticker_size // 2,
                        screen_sticker_size,
                        screen_sticker_size
                    )
                    pygame.draw.rect(screen, color, sticker_rect)
                    pygame.draw.rect(screen, COLORS['deepcharcoal'], sticker_rect, 1)
            
            # Draw face edges (optional, for better visibility)
            vertices = self._get_face_vertices(face_name)
            if vertices:
                projected_vertices = [self._project_3d_to_2d(v[0], v[1], v[2]) for v in vertices]
                # Draw edges (only for visible faces)
                if face_name in ['front', 'right', 'top']:  # Most visible faces
                    for i in range(4):
                        start = projected_vertices[i]
                        end = projected_vertices[(i + 1) % 4]
                        pygame.draw.line(
                            screen,
                            COLORS['deepcharcoal'],
                            start,
                            end,
                            1
                        )

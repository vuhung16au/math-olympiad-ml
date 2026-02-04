"""Graph renderer for Rubik's Cube - planar graph visualization.

This module provides a foundation for rendering the cube as a planar graph
with 54 dots representing stickers, connected by edges.
"""

import pygame
import math
from typing import Tuple
from core.cube_state import CubeState
from visualization.flat_renderer import COLORS, CUBE_COLORS


class GraphRenderer:
    """Renders the cube as a planar graph with dots and edges."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize renderer with screen dimensions.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.update_layout()
        self._initialize_graph_positions()
    
    def update_layout(self):
        """Update layout based on current screen size."""
        # Leave space for UI: left side (instructions) ~250px, bottom (log) ~80px, right (buttons) ~150px
        left_margin = 250
        right_margin = 150
        bottom_margin = 80
        top_margin = 50
        available_width = self.screen_width - left_margin - right_margin
        available_height = self.screen_height - top_margin - bottom_margin
        
        # Center of the graph (in available space)
        self.center_x = left_margin + available_width // 2
        self.center_y = top_margin + available_height // 2
        # Radius for sticker placement (will be arranged in a circle pattern as placeholder)
        self.radius = min(available_width, available_height) // 3
        # Dot size
        self.dot_size = max(8, min(available_width, available_height) // 60)
    
    def _initialize_graph_positions(self):
        """Initialize positions for 54 stickers in graph layout.
        
        This is a placeholder implementation. A full implementation would
        calculate positions based on the actual planar graph structure.
        """
        self.sticker_positions = []
        # Placeholder: arrange in concentric circles
        # Face 0 (Top): inner circle
        for i in range(9):
            angle = 2 * math.pi * i / 9
            x = self.center_x + self.radius * 0.3 * math.cos(angle)
            y = self.center_y + self.radius * 0.3 * math.sin(angle)
            self.sticker_positions.append((x, y))
        
        # Face 1 (Bottom): second circle
        for i in range(9):
            angle = 2 * math.pi * i / 9 + math.pi / 9
            x = self.center_x + self.radius * 0.5 * math.cos(angle)
            y = self.center_y + self.radius * 0.5 * math.sin(angle)
            self.sticker_positions.append((x, y))
        
        # Faces 2-5 (Front, Back, Left, Right): outer circles
        for face_offset in range(4):
            for i in range(9):
                angle = 2 * math.pi * (i + face_offset * 2.25) / 9 + math.pi / 4
                x = self.center_x + self.radius * 0.8 * math.cos(angle)
                y = self.center_y + self.radius * 0.8 * math.sin(angle)
                self.sticker_positions.append((x, y))
    
    def set_screen_size(self, width: int, height: int):
        """Update screen size and recalculate layout.
        
        Args:
            width: New screen width
            height: New screen height
        """
        self.screen_width = width
        self.screen_height = height
        self.update_layout()
        self._initialize_graph_positions()
    
    def draw(self, screen: pygame.Surface, cube: CubeState):
        """Draw the cube as a planar graph.
        
        Args:
            screen: Pygame surface to draw on
            cube: CubeState to render
        """
        # Draw edges (placeholder - would show actual graph structure)
        # For now, skip edge drawing as it requires full graph layout
        
        # Draw dots for each sticker
        for i in range(54):
            color_char = cube.get_sticker(i)
            color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
            x, y = self.sticker_positions[i]
            
            # Draw dot
            pygame.draw.circle(
                screen,
                color,
                (int(x), int(y)),
                self.dot_size
            )
            # Draw border
            pygame.draw.circle(
                screen,
                COLORS['deepcharcoal'],
                (int(x), int(y)),
                self.dot_size,
                1
            )

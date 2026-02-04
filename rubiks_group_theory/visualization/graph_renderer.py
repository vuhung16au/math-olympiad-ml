"""Graph renderer for Rubik's Cube - planar graph visualization.

This module provides a foundation for rendering the cube as a planar graph
with 54 dots representing stickers, connected by edges.
"""

import pygame
import math
from typing import Tuple, List, Set
from core.cube_state import CubeState
from visualization.flat_renderer import COLORS, CUBE_COLORS


def get_adjacent_stickers() -> List[List[int]]:
    """Get adjacency list for all 54 stickers.
    
    Returns:
        List of 54 lists, where each list contains indices of adjacent stickers
    """
    adj = [[] for _ in range(54)]
    
    # Face starts: Top=0, Bottom=9, Front=18, Back=27, Left=36, Right=45
    face_starts = [0, 9, 18, 27, 36, 45]
    
    # Helper: get row and column from position in a face
    def get_pos_in_face(global_idx):
        for face_start in face_starts:
            if face_start <= global_idx < face_start + 9:
                local_idx = global_idx - face_start
                row = local_idx // 3
                col = local_idx % 3
                return face_start, row, col
        return None, None, None
    
    # Within each face: connect horizontal and vertical neighbors
    for face_start in face_starts:
        for row in range(3):
            for col in range(3):
                idx = face_start + row * 3 + col
                # Right neighbor
                if col < 2:
                    adj[idx].append(face_start + row * 3 + col + 1)
                # Left neighbor
                if col > 0:
                    adj[idx].append(face_start + row * 3 + col - 1)
                # Bottom neighbor
                if row < 2:
                    adj[idx].append(face_start + (row + 1) * 3 + col)
                # Top neighbor
                if row > 0:
                    adj[idx].append(face_start + (row - 1) * 3 + col)
    
    # Between faces: connect edge stickers
    # Top face (0-8) edges:
    # Top row (0,1,2) connects to Back top row (27,28,29) - reversed
    for i in range(3):
        adj[0 + i].append(27 + (2 - i))  # Reversed
        adj[27 + (2 - i)].append(0 + i)
    # Right column (2,5,8) connects to Right top row (45,46,47)
    adj[2].append(45); adj[45].append(2)
    adj[5].append(46); adj[46].append(5)
    adj[8].append(47); adj[47].append(8)
    # Bottom row (6,7,8) connects to Front top row (18,19,20)
    for i in range(3):
        adj[6 + i].append(18 + i)
        adj[18 + i].append(6 + i)
    # Left column (0,3,6) connects to Left top row (36,37,38)
    adj[0].append(36); adj[36].append(0)
    adj[3].append(37); adj[37].append(3)
    adj[6].append(38); adj[38].append(6)
    
    # Bottom face (9-17) edges:
    # Bottom row (15,16,17) connects to Back bottom row (33,34,35) - reversed
    for i in range(3):
        adj[15 + i].append(33 + (2 - i))
        adj[33 + (2 - i)].append(15 + i)
    # Right column (11,14,17) connects to Right bottom row (51,52,53)
    adj[11].append(51); adj[51].append(11)
    adj[14].append(52); adj[52].append(14)
    adj[17].append(53); adj[53].append(17)
    # Top row (9,10,11) connects to Front bottom row (24,25,26)
    for i in range(3):
        adj[9 + i].append(24 + i)
        adj[24 + i].append(9 + i)
    # Left column (9,12,15) connects to Left bottom row (42,43,44)
    adj[9].append(42); adj[42].append(9)
    adj[12].append(43); adj[43].append(12)
    adj[15].append(44); adj[44].append(15)
    
    # Front face (18-26) edges:
    # Right column (20,23,26) connects to Right left column (45,48,51)
    adj[20].append(45); adj[45].append(20)
    adj[23].append(48); adj[48].append(23)
    adj[26].append(51); adj[51].append(26)
    # Left column (18,21,24) connects to Left right column (38,41,44)
    adj[18].append(38); adj[38].append(18)
    adj[21].append(41); adj[41].append(21)
    adj[24].append(44); adj[44].append(24)
    
    # Back face (27-35) edges:
    # Right column (29,32,35) connects to Left left column (36,39,42) - reversed
    adj[29].append(42); adj[42].append(29)
    adj[32].append(39); adj[39].append(32)
    adj[35].append(36); adj[36].append(35)
    # Left column (27,30,33) connects to Right right column (47,50,53) - reversed
    adj[27].append(53); adj[53].append(27)
    adj[30].append(50); adj[50].append(30)
    adj[33].append(47); adj[47].append(33)
    
    # Remove duplicates
    for i in range(54):
        adj[i] = list(set(adj[i]))
    
    return adj


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
        self.adjacency_list = get_adjacent_stickers()
        self.update_layout()
        self._initialize_graph_positions()
    
    def update_layout(self):
        """Update layout based on current screen size."""
        # Layout: Graph view on the LEFT side, 3D render on the RIGHT side
        # Leave space for UI: left side (instructions) ~250px, bottom (log) ~80px
        left_margin = 250  # Space for instructions
        bottom_margin = 80  # Space for log
        top_margin = 50
        
        # Calculate the split point: graph on left, 3D on right
        # Use approximately 50% of screen for graph, 50% for 3D (after margins)
        split_point = left_margin + (self.screen_width - left_margin - 150) // 2  # 150px for buttons
        
        # Graph view uses the left portion (from left_margin to split_point)
        graph_left = left_margin
        graph_right = split_point
        graph_width = graph_right - graph_left
        available_height = self.screen_height - top_margin - bottom_margin
        
        # Center of the graph (in its left portion)
        self.center_x = graph_left + graph_width // 2
        self.center_y = top_margin + available_height // 2
        
        # Radius for sticker placement - use the smaller dimension
        self.radius = min(graph_width, available_height) // 3
        # Dot size - make them larger for better visibility
        self.dot_size = max(6, min(graph_width, available_height) // 50)
    
    def _initialize_graph_positions(self):
        """Initialize positions for 54 stickers in graph layout.
        
        Arranges stickers in a structured way: each face's stickers are grouped
        together in compact 3x3 grids, and the 6 faces are arranged in a circle.
        """
        self.sticker_positions = []
        
        # Face order: Top=0, Bottom=1, Front=2, Back=3, Left=4, Right=5
        # Arrange 6 faces in a regular hexagon pattern
        face_angles = [
            -math.pi / 2,           # 0: Top (up)
            math.pi / 2,            # 1: Bottom (down)
            0,                      # 2: Front (right)
            math.pi,                # 3: Back (left)
            -math.pi / 3,           # 4: Left (lower-right)
            -2 * math.pi / 3,       # 5: Right (lower-left)
        ]
        
        # Distance from center for face centers - make it larger for better separation
        face_radius = self.radius * 0.7
        
        # Size of each face's 3x3 grid (spacing between stickers)
        # Make grids more compact
        sticker_spacing = self.radius * 0.1
        
        # Process each face
        for face_idx in range(6):
            face_start = face_idx * 9
            face_angle = face_angles[face_idx]
            
            # Center of this face's grid
            face_center_x = self.center_x + face_radius * math.cos(face_angle)
            face_center_y = self.center_y + face_radius * math.sin(face_angle)
            
            # Arrange 9 stickers in a 3x3 grid
            for row in range(3):
                for col in range(3):
                    sticker_idx = face_start + row * 3 + col
                    
                    # Position within face grid (3x3)
                    # Center the grid: positions go from -spacing to +spacing
                    offset_x = (col - 1) * sticker_spacing
                    offset_y = (row - 1) * sticker_spacing
                    
                    # Apply rotation based on face angle to orient grids nicely
                    # Rotate all grids to face outward from center
                    rot_angle = face_angle
                    rotated_x = offset_x * math.cos(rot_angle) - offset_y * math.sin(rot_angle)
                    rotated_y = offset_x * math.sin(rot_angle) + offset_y * math.cos(rot_angle)
                    
                    x = face_center_x + rotated_x
                    y = face_center_y + rotated_y
                    
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
        # Draw edges first (so dots appear on top)
        # Use a lighter color for better visibility
        edge_color = COLORS['warmstone']
        edge_alpha = 80  # More visible edges
        edge_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        
        # Only draw edges within faces and between adjacent faces (not all connections)
        # This reduces visual clutter
        for i in range(54):
            x1, y1 = self.sticker_positions[i]
            for neighbor in self.adjacency_list[i]:
                if neighbor > i:  # Draw each edge only once
                    x2, y2 = self.sticker_positions[neighbor]
                    
                    # Draw edge (show all connections for now)
                    pygame.draw.line(
                        edge_surface,
                        (*edge_color, edge_alpha),
                        (int(x1), int(y1)),
                        (int(x2), int(y2)),
                        1  # Thin lines
                    )
        
        screen.blit(edge_surface, (0, 0))
        
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

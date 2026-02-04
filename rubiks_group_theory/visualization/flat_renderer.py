"""Flat renderer for Rubik's Cube - unfolded cross view.

This module renders the cube in the standard "unfolded cross" layout.
"""

import pygame
import math
from typing import Tuple, Optional, Dict, List
from core.cube_state import CubeState
from core.permutations import MOVES



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
    'canvasgray': (224, 220, 214),
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
    
    def _get_pos_for_index(self, index: int) -> Tuple[int, int]:
        """Get the screen (x, y) coordinates for a given sticker index.
        
        Args:
            index: Sticker index (0-53)
            
        Returns:
            (x, y) coordinates of the top-left corner of the sticker
        """
        # Determine face and internal index
        face_starts = {0: 'top', 9: 'bottom', 18: 'front', 27: 'back', 36: 'left', 45: 'right'}
        
        # Find which face range this index belongs to
        start_idx = 0
        face_name = 'top'
        for start in sorted(face_starts.keys()):
            if index >= start:
                start_idx = start
                face_name = face_starts[start]
        
        local_idx = index - start_idx
        row = local_idx // 3
        col = local_idx % 3
        
        # Map face to grid layout
        layout = {
            'top': (1, 0),      # Column 1, Row 0
            'left': (0, 1),     # Column 0, Row 1
            'front': (1, 1),   # Column 1, Row 1
            'right': (2, 1),    # Column 2, Row 1
            'back': (3, 1),    # Column 3, Row 1
            'bottom': (1, 2),  # Column 1, Row 2
        }
        
        grid_x, grid_y = layout[face_name]
        
        x = self.offset_x + grid_x * 3 * self.sticker_size + col * self.sticker_size
        y = self.offset_y + grid_y * 3 * self.sticker_size + row * self.sticker_size
        
        return int(x), int(y)

    def draw(self, screen: pygame.Surface, cube: CubeState, animation_state: Optional[Dict] = None):
        """Draw the cube in unfolded cross view.
        
        Args:
            screen: Pygame surface to draw on
            cube: CubeState to render
            animation_state: Optional dict with keys 'move' (str) and 'progress' (float 0-1)
        """
        # If animating, we draw stickers at interpolated positions
        if animation_state and animation_state.get('move'):
            self._draw_animated(screen, cube, animation_state['move'], animation_state['progress'])
            return

        # Normal static drawing
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

    
    def _rotate_point(self, point: Tuple[float, float], center: Tuple[float, float], angle_degrees: float) -> Tuple[float, float]:
        """Rotate a point around a center."""
        x, y = point
        cx, cy = center
        
        # Convert to radians
        # Screen coords: positive angle is clockwise generally, BUT
        # standard math: CCW is positive X->Y. 
        # In pygame (Y down), positive angle in sin/cos logic is CW visually?
        # Let's use radians.
        rad = math.radians(angle_degrees)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        # Translate to origin
        tx = x - cx
        ty = y - cy
        
        # Rotate
        rx = tx * cos_a - ty * sin_a
        ry = tx * sin_a + ty * cos_a
        
        return (rx + cx, ry + cy)

    def _get_face_center(self, face_name: str) -> Tuple[int, int]:
        """Get the center coordinates of a face."""
        layout = {
            'top': (1, 0),
            'left': (0, 1),
            'front': (1, 1),
            'right': (2, 1),
            'back': (3, 1),
            'bottom': (1, 2),
        }
        grid_x, grid_y = layout[face_name]
        
        # Center is at top-left of face + 1.5 * sticker_size * 3 (no wait, 3 stickers)
        # Face width = 3 * sticker_size
        face_x = self.offset_x + grid_x * 3 * self.sticker_size
        face_y = self.offset_y + grid_y * 3 * self.sticker_size
        
        center_x = face_x + (1.5 * self.sticker_size)
        center_y = face_y + (1.5 * self.sticker_size)
        return int(center_x), int(center_y)

    def _draw_polygon_sticker(self, screen: pygame.Surface, points: List[Tuple[float, float]], color: tuple):
        """Draw a sticker defined by 4 points."""
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, COLORS['deepcharcoal'], points, 2)

    def _draw_animated(self, screen: pygame.Surface, cube: CubeState, move_name: str, progress: float):
        """Draw cube in animated state with realistic rotations."""
        # Define move properties
        # (Active Face, Rotation degrees for CW)
        move_props = {
            'U': ('top', -90), "U'": ('top', 90),
            'D': ('bottom', 90), "D'": ('bottom', -90), # D is CW looking from bottom, so CCW looking from front? No, wait. 
            # D (Clockwise bottom) moves Front -> Right.
            # Grid: Front(1,1) -> Right(2,1). X increases.
            # Bottom face center: (1,2).
            # Stickers on bottom face: 
            # Let's normalize everything to "Face Rotation" + "Belt Movement".
            
            # Simple rotation direction check:
            # U: Top face rotates CW.
            # U': Top face rotates CCW.
            # D: Bottom face rotates CW.
            # F: Front face rotates CW.
            # B: Back face rotates CW.
            # R: Right face rotates CW.
            # L: Left face rotates CW.
            
            'R': ('right', -90), "R'": ('right', 90),
            'L': ('left', -90), "L'": ('left', 90),
            'F': ('front', -90), "F'": ('front', 90),
            'B': ('back', -90), "B'": ('back', 90),
        }
        
        base_move = move_name.replace("'", "")
        active_face, angle_total = move_props[move_name]
        
        # Current rotation angle
        angle = angle_total * progress
        
        # Get face center
        center = self._get_face_center(active_face)
        
        # Face indices (0-8 relative to face start)
        face_starts = {'top': 0, 'bottom': 9, 'front': 18, 'back': 27, 'left': 36, 'right': 45}
        start_idx = face_starts[active_face]
        face_indices = list(range(start_idx, start_idx + 9))
        
        # Belt indices handling
        # Define belts for each move type
        # For F/B: It's a ring.
        # For U/D: It's a horizontal ring (with wrap).
        # For L/R: It's a "vertical" ring (disjoint in 2D).
        
        belt_indices = []
        is_ring = False
        
        if base_move in ['F', 'B']:
            is_ring = True
            if base_move == 'F':
                # F Belt: Top(6,7,8) -> Right(0,3,6) -> Bottom(2,1,0) -> Left(8,5,2)
                # Wait, indices are cleaner in permutations.py, let's just grab involved stickers
                # F affects: Top rows 6,7,8; Right cols 0,3,6 (local? No global indices)
                # Global: Top(6,7,8), Right(45,48,51), Bottom(9,10,11), Left(44,41,38)
                belt_indices = [6,7,8, 45,48,51, 9,10,11, 44,41,38]
            else: # B
                # B affects: Top(0,1,2), Left(36,39,42), Bottom(15,16,17), Right(53,50,47)
                belt_indices = [0,1,2, 36,39,42, 15,16,17, 53,50,47]
        
        # Indices to treat as rigid body (Face + Ring if applicable)
        rigid_indices = set(face_indices)
        if is_ring:
            rigid_indices.update(belt_indices)
            
        # 1. Draw all static stickers (not involved in move)
        # We need to list involved indices first
        involved_indices = set(face_indices)
        
        # Get perm to know all affected stickers
        if move_name in MOVES:
            perm = MOVES[move_name]()
            # Any sticker where perm[i] != i is involved
            for i in range(54):
                if perm[i] != i:
                    involved_indices.add(i)
        
        # Draw static stickers
        for i in range(54):
            if i not in involved_indices:
                color_char = cube.get_sticker(i)
                color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
                x, y = self._get_pos_for_index(i)
                rect = pygame.Rect(x, y, self.sticker_size - 2, self.sticker_size - 2)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, COLORS['deepcharcoal'], rect, 1)

        # 2. Draw Rigid Body Rotation (Face + potentially Ring)
        for i in rigid_indices:
            color_char = cube.get_sticker(i)
            color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
            
            # Get original 4 corners
            sx, sy = self._get_pos_for_index(i)
            s = self.sticker_size - 2
            corners = [
                (sx, sy), (sx + s, sy),
                (sx + s, sy + s), (sx, sy + s)
            ]
            
            # Rotate corners around face center
            rotated_corners = [self._rotate_point(p, center, angle) for p in corners]
            
            self._draw_polygon_sticker(screen, rotated_corners, color)
            
        # 3. Draw Belt Sliding (If not handled as ring)
        # For U, D, L, R
        if not is_ring:
            remaining_belt = involved_indices - rigid_indices
            
            if base_move in ['U', 'D']:
                self._draw_horizontal_belt(screen, cube, list(remaining_belt), move_name, progress)
            elif base_move in ['L', 'R']:
                self._draw_vertical_belt(screen, cube, list(remaining_belt), move_name, progress)


    def _draw_horizontal_belt(self, screen, cube, indices, move_name, progress):
        """Draw horizontal belt animation (U/D moves) with wrap-around."""
        # Get target positions from permutation
        perm = MOVES[move_name]()
        total_width = 4 * 3 * self.sticker_size # 4 faces wide
        
        for i in indices:
            color_char = cube.get_sticker(i)
            color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
            
            start_x, start_y = self._get_pos_for_index(i)
            dest_idx = perm[i]
            end_x, end_y = self._get_pos_for_index(dest_idx)
            
            # Handle wrap around
            # Grid layout order X: Left(0), Front(1), Right(2), Back(3)
            # U move (CW): Front -> Left. X decreases.
            # Left(0) has x ~ 250. Back(3) has x ~ 250 + 3*width.
            
            # Determine direction based on move
            # U: Right to Left (visual slide left). Delta X approx negative.
            # U': Left to Right. Delta X positive.
            # D: Left to Right. (Bottom face CW = Right moves to Back? No. D moves Front -> Right).
            # Wait. D (CW) moves F(24,25,26) -> R(51,52,53). Front is Left of Right. So moves Right.
            
            dx = end_x - start_x
            
            # Check for wrap-around jump
            # If distance is > 2 face widths, it's a wrap
            face_w = 3 * self.sticker_size
            
            virtual_end_x = end_x
            
            if abs(dx) > 2 * face_w:
                # Wrap detected
                if dx > 0: # Jumping Right -> Left (large positive gap? No. 0 -> 3 is large pos)
                    # Example: Back(3) -> Right(2). X goes 3->2. dx negative small.
                    # Example: Left(0) -> Back(3). X goes 0->3. dx positive large.
                    # Visual: Should move Left -> "Left of Left".
                    virtual_end_x = end_x - total_width
                else: 
                    # Jumping Left -> Right (large negative gap)
                    # Example: Back(3) -> Left(0). X goes 3->0. dx negative large.
                    # Visual: Should move Right -> "Right of Right".
                    virtual_end_x = end_x + total_width
            
            # Interpolate
            curr_x = start_x + (virtual_end_x - start_x) * progress
            curr_y = start_y # Y should be constant for U/D belts
            
            # Wrap visual coord to screen bounds (optional, but clip rect handles it usually)
            # But we want to draw it appearing on the other side?
            # Actually simpler: Draw twice if near edge? 
            # Or just let it slide off and rely on the other one sliding in.
            # With linear interpolation of 'virtual_end', it slides smoothly.
            # But the one appearing?
            # The sticker appearing at 'end_x' comes from 'start_x' (virtualized).
            
            draw_pos_x = curr_x
            
            # Draw
            rect = pygame.Rect(draw_pos_x, curr_y, self.sticker_size - 2, self.sticker_size - 2)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLORS['deepcharcoal'], rect, 1)


    def _draw_vertical_belt(self, screen, cube, indices, move_name, progress):
        """Draw vertical belt animation (L/R moves)."""
        # For L/R, the 2D layout splits them disjointly.
        # Top -> Front -> Bottom is linear vertical.
        # But Bottom -> Back is a jump. Back -> Top is a jump.
        # We'll just use simple linear interpolation. It will look like flying across for the jumps.
        # Unless we implement virtual coordinates for these too.
        # Back is grid (3, 1). Top is (1, 0). Front (1, 1). Bottom (1, 2).
        # R move: Top -> Back.. wait.
        # R (Right Face CW): Top(2,5,8) -> Back(30,33,36).
        # Top(1,0) -> Back(3,1). Diagonal jump.
        # Back -> Bottom(1,2). Diagonal jump.
        # Bottom -> Front(1,1). Vertical Up.
        # Front -> Top(1,0). Vertical Up.
        
        # So Front->Top and Bottom->Front are clean vertical slides.
        # The interactions with Back are jumps.
        # Let's just use linear interp for now.
        
        perm = MOVES[move_name]()
        
        for i in indices:
            color_char = cube.get_sticker(i)
            color = CUBE_COLORS.get(color_char, COLORS['bookblack'])
            
            start_x, start_y = self._get_pos_for_index(i)
            dest_idx = perm[i]
            end_x, end_y = self._get_pos_for_index(dest_idx)
            
            curr_x = start_x + (end_x - start_x) * progress
            curr_y = start_y + (end_y - start_y) * progress
            
            rect = pygame.Rect(curr_x, curr_y, self.sticker_size - 2, self.sticker_size - 2)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, COLORS['deepcharcoal'], rect, 1)




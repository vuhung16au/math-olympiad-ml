"""3D renderer for Rubik's Cube with per-sticker depth sorting."""

import math
from typing import Dict, List, Optional, Tuple

import pygame

from core.cube_state import CubeState
from visualization.flat_renderer import COLORS, CUBE_COLORS


class Cube3DRenderer:
    """Renders the cube in 3D (front/left/top visible faces)."""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Interactive camera.
        self.rot_x = 30
        self.rot_y = -45
        self.zoom = 1.0

        self.update_geometry()

    def set_rotation(self, rx: float, ry: float):
        """Set camera rotation angles in degrees."""
        self.rot_x = rx
        self.rot_y = ry

    def update_geometry(self):
        """Update panel placement and sizing."""
        left_margin = 250
        right_margin = 150
        split_point = left_margin + (self.screen_width - left_margin - right_margin) // 2

        cube_left = split_point
        cube_right = self.screen_width - right_margin
        cube_width = cube_right - cube_left
        available_height = self.screen_height - 80

        self.center_x = cube_left + cube_width // 2
        self.center_y = self.screen_height // 2
        self.sticker_size = min(cube_width // 12, available_height // 12, 50)

    def set_screen_size(self, width: int, height: int):
        """Update screen size and recalculate geometry."""
        self.screen_width = width
        self.screen_height = height
        self.update_geometry()

    def _rotate_view(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Apply camera yaw then pitch; returns view-space coordinates."""
        yaw = math.radians(self.rot_y)
        cos_y = math.cos(yaw)
        sin_y = math.sin(yaw)

        x1 = x * cos_y - z * sin_y
        z1 = x * sin_y + z * cos_y
        y1 = y

        pitch = math.radians(self.rot_x)
        cos_x = math.cos(pitch)
        sin_x = math.sin(pitch)

        y2 = y1 * cos_x - z1 * sin_x
        z2 = y1 * sin_x + z1 * cos_x
        x2 = x1

        return x2, y2, z2

    def _project(self, x_view: float, y_view: float) -> Tuple[int, int]:
        """Project view-space point to screen."""
        return (
            self.center_x + int(x_view * self.zoom),
            self.center_y - int(y_view * self.zoom),
        )

    def _rotate_axis(
        self, x: float, y: float, z: float, axis: str, angle_deg: float
    ) -> Tuple[float, float, float]:
        """Rotate world-space point around one axis."""
        a = math.radians(angle_deg)
        c = math.cos(a)
        s = math.sin(a)

        if axis == "x":
            return x, y * c - z * s, y * s + z * c
        if axis == "y":
            return x * c + z * s, y, -x * s + z * c
        return x * c - y * s, x * s + y * c, z

    def _get_sticker_corners_3d(
        self, face_name: str, row: int, col: int, sticker_size: float, gap: float
    ) -> List[Tuple[float, float, float]]:
        """Return world-space corners for a face sticker."""
        s = sticker_size
        half = (s - gap) / 2

        x_offset = (col - 1) * s
        y_offset = (1 - row) * s
        local_corners = [
            (x_offset - half, y_offset + half),
            (x_offset + half, y_offset + half),
            (x_offset + half, y_offset - half),
            (x_offset - half, y_offset - half),
        ]

        face_offset = 1.5 * s
        corners_3d: List[Tuple[float, float, float]] = []

        if face_name == "front":
            for lx, ly in local_corners:
                corners_3d.append((lx, ly, face_offset))
        elif face_name == "left":
            for lx, ly in local_corners:
                corners_3d.append((-face_offset, ly, -lx))
        elif face_name == "top":
            for lx, ly in local_corners:
                corners_3d.append((lx, face_offset, ly))

        return corners_3d

    def _sticker_center(
        self, corners: List[Tuple[float, float, float]]
    ) -> Tuple[float, float, float]:
        """Average center point of a sticker polygon."""
        n = len(corners)
        return (
            sum(p[0] for p in corners) / n,
            sum(p[1] for p in corners) / n,
            sum(p[2] for p in corners) / n,
        )

    def _is_in_moving_layer(
        self, center: Tuple[float, float, float], base_move: str, threshold: float
    ) -> bool:
        """Check if sticker belongs to the rotating layer for a move."""
        x, y, z = center

        if base_move == "U":
            return y > threshold
        if base_move == "D":
            return y < -threshold
        if base_move == "R":
            return x > threshold
        if base_move == "L":
            return x < -threshold
        if base_move == "F":
            return z > threshold
        if base_move == "B":
            return z < -threshold
        return False

    def _animation_spec(
        self, animation_state: Optional[Dict]
    ) -> Optional[Tuple[str, str, float]]:
        """Decode animation state into (base_move, axis, angle)."""
        if not animation_state:
            return None

        move = animation_state.get("move")
        progress = animation_state.get("progress")
        if not move or progress is None:
            return None

        move_angles = {
            "U": -90,
            "U'": 90,
            "D": 90,
            "D'": -90,
            "R": -90,
            "R'": 90,
            "L": -90,
            "L'": 90,
            "F": -90,
            "F'": 90,
            "B": -90,
            "B'": 90,
        }
        base_move = move.replace("'", "")
        axis_map = {"U": "y", "D": "y", "R": "x", "L": "x", "F": "z", "B": "z"}
        if move not in move_angles or base_move not in axis_map:
            return None

        return base_move, axis_map[base_move], move_angles[move] * float(progress)

    def draw(
        self,
        screen: pygame.Surface,
        cube: CubeState,
        animation_state: Optional[Dict] = None,
    ):
        """Draw cube with painter's algorithm and optional smooth turn animation."""
        faces = {
            "top": cube.get_face("top"),
            "left": cube.get_face("left"),
            "front": cube.get_face("front"),
        }
        face_order = ["top", "left", "front"]
        gap = self.sticker_size * 0.05

        anim = self._animation_spec(animation_state)
        layer_threshold = 0.5 * self.sticker_size

        draw_items = []
        for face_name in face_order:
            face = faces[face_name]
            for row in range(3):
                for col in range(3):
                    color_char = face[row][col]
                    color = CUBE_COLORS.get(color_char, COLORS["bookblack"])

                    corners = self._get_sticker_corners_3d(
                        face_name, row, col, self.sticker_size, gap
                    )

                    if anim is not None:
                        base_move, axis, angle = anim
                        center = self._sticker_center(corners)
                        if self._is_in_moving_layer(center, base_move, layer_threshold):
                            corners = [
                                self._rotate_axis(x, y, z, axis, angle)
                                for x, y, z in corners
                            ]

                    view_corners = [self._rotate_view(x, y, z) for x, y, z in corners]
                    screen_corners = [self._project(x, y) for x, y, _ in view_corners]
                    avg_depth = sum(z for _, _, z in view_corners) / 4.0

                    draw_items.append(
                        {
                            "depth": avg_depth,
                            "corners": screen_corners,
                            "color": color,
                        }
                    )

        # Painter's algorithm: far stickers first, near stickers last.
        draw_items.sort(key=lambda item: item["depth"])

        for item in draw_items:
            pygame.draw.polygon(screen, item["color"], item["corners"])
            pygame.draw.polygon(screen, COLORS["deepcharcoal"], item["corners"], 2)

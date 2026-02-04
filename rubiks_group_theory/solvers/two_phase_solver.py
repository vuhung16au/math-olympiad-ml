"""Two-phase solver wrapper (Kociemba) with app-friendly move output."""

from __future__ import annotations

from typing import List

from core.cube_state import CubeState


class TwoPhaseSolver:
    """Solve a cube using Kociemba's two-phase algorithm when available."""

    def __init__(self):
        self._kociemba = None
        self._import_error = None
        self.phases = [(0, "Two-Phase: Kociemba Search")]

        try:
            import kociemba  # type: ignore

            self._kociemba = kociemba
        except Exception as exc:  # pragma: no cover - environment-dependent
            self._import_error = str(exc)

    def is_available(self) -> bool:
        """Return True when the optional kociemba package is importable."""
        return self._kociemba is not None

    def availability_reason(self) -> str:
        """Explain why two-phase solver is unavailable."""
        if self.is_available():
            return "available"
        if self._import_error:
            return self._import_error
        return "kociemba package not installed"

    def solve(self, cube: CubeState) -> List[str]:
        """Compute a solve sequence and normalize to quarter-turn tokens."""
        if not self.is_available():
            raise RuntimeError(
                "Two-phase solver unavailable. Install dependency: pip install kociemba"
            )

        cube_string = self._to_kociemba_facelets(cube)
        # API returns tokens like: "R U R' U' F2 ..."
        solution = self._kociemba.solve(cube_string)
        return self._expand_half_turns(solution)

    def _to_kociemba_facelets(self, cube: CubeState) -> str:
        """Convert internal cube colors to the URFDLB facelet string."""
        face_order = [
            ("top", "U"),
            ("right", "R"),
            ("front", "F"),
            ("bottom", "D"),
            ("left", "L"),
            ("back", "B"),
        ]
        color_to_face = {
            "W": "U",
            "R": "R",
            "G": "F",
            "Y": "D",
            "O": "L",
            "B": "B",
        }

        out = []
        for face_name, _ in face_order:
            face = cube.get_face(face_name)
            for row in face:
                for color in row:
                    mapped = color_to_face.get(color)
                    if mapped is None:
                        raise ValueError(f"Invalid color '{color}' in cube state")
                    out.append(mapped)
        return "".join(out)

    def _expand_half_turns(self, solution: str) -> List[str]:
        """Expand tokens with '2' into two quarter turns for animation pipeline."""
        if not solution.strip():
            return []

        expanded: List[str] = []
        for token in solution.split():
            if token.endswith("2"):
                base = token[:-1]
                expanded.extend([base, base])
            else:
                expanded.append(token)
        return expanded


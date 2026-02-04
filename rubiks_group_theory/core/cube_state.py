"""Cube state representation with 54-sticker indexing system.

This module provides the data structure for representing a Rubik's Cube
with both sticker-based (for permutations) and face-based (for compatibility) interfaces.
"""


class CubeState:
    """Represents a Rubik's Cube state with 54 stickers.
    
    Each face has 9 stickers, indexed as follows:
    - Face order: Top, Bottom, Front, Back, Left, Right
    - Sticker indexing within each face (3x3):
        0 1 2
        3 4 5
        6 7 8
    - Global sticker indices: 0-53 (6 faces × 9 stickers)
    """
    
    # Face colors
    WHITE = 'W'
    YELLOW = 'Y'
    GREEN = 'G'
    BLUE = 'B'
    ORANGE = 'O'
    RED = 'R'
    
    def __init__(self):
        """Initialize a solved cube state."""
        # Initialize as 54-element list (sticker-based representation)
        # Face order: Top, Bottom, Front, Back, Left, Right
        # Each face: 9 stickers in row-major order
        self.stickers = [
            # Top face (0-8): White
            'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W',
            # Bottom face (9-17): Yellow
            'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y',
            # Front face (18-26): Green
            'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
            # Back face (27-35): Blue
            'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B',
            # Left face (36-44): Orange
            'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',
            # Right face (45-53): Red
            'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R',
        ]
    
    def get_sticker(self, index: int) -> str:
        """Get sticker color at given index (0-53)."""
        if not 0 <= index < 54:
            raise ValueError(f"Sticker index must be between 0 and 53, got {index}")
        return self.stickers[index]
    
    def set_sticker(self, index: int, color: str):
        """Set sticker color at given index (0-53)."""
        if not 0 <= index < 54:
            raise ValueError(f"Sticker index must be between 0 and 53, got {index}")
        self.stickers[index] = color
    
    def get_face(self, face_name: str) -> list:
        """Get face as 3x3 list (backward compatibility).
        
        Args:
            face_name: One of 'top', 'bottom', 'front', 'back', 'left', 'right'
        
        Returns:
            3x3 list of colors
        """
        face_map = {
            'top': 0,
            'bottom': 9,
            'front': 18,
            'back': 27,
            'left': 36,
            'right': 45,
        }
        
        if face_name not in face_map:
            raise ValueError(f"Invalid face name: {face_name}")
        
        start_idx = face_map[face_name]
        face = []
        for row in range(3):
            face.append([
                self.stickers[start_idx + row * 3 + col]
                for col in range(3)
            ])
        return face
    
    def set_face(self, face_name: str, face_data: list):
        """Set face from 3x3 list (backward compatibility).
        
        Args:
            face_name: One of 'top', 'bottom', 'front', 'back', 'left', 'right'
            face_data: 3x3 list of colors
        """
        face_map = {
            'top': 0,
            'bottom': 9,
            'front': 18,
            'back': 27,
            'left': 36,
            'right': 45,
        }
        
        if face_name not in face_map:
            raise ValueError(f"Invalid face name: {face_name}")
        
        if len(face_data) != 3 or any(len(row) != 3 for row in face_data):
            raise ValueError("Face data must be a 3x3 list")
        
        start_idx = face_map[face_name]
        for row in range(3):
            for col in range(3):
                self.stickers[start_idx + row * 3 + col] = face_data[row][col]
    
    def apply_permutation(self, permutation: list):
        """Apply a permutation to the cube state.
        
        Args:
            permutation: List of 54 integers representing where each sticker moves.
                        permutation[i] = j means sticker at position i moves to position j.
        """
        if len(permutation) != 54:
            raise ValueError("Permutation must have exactly 54 elements")
        
        # Validate permutation covers all positions
        covered = set(permutation)
        if len(covered) != 54 or min(covered) != 0 or max(covered) != 53:
            missing = set(range(54)) - covered
            duplicates = [i for i in range(54) if permutation.count(i) > 1]
            raise ValueError(
                f"Invalid permutation: covers {len(covered)}/54 positions. "
                f"Missing: {missing}, Duplicates: {duplicates}"
            )
        
        # Create new state by applying permutation
        new_stickers = [''] * 54
        for i in range(54):
            dest = permutation[i]
            if not (0 <= dest < 54):
                raise ValueError(f"Invalid destination {dest} at position {i}")
            new_stickers[dest] = self.stickers[i]
        
        # Validate no empty strings remain (should never happen with valid permutation)
        empty_positions = [i for i, s in enumerate(new_stickers) if not s]
        if empty_positions:
            raise ValueError(f"Permutation resulted in empty sticker positions: {empty_positions}")
        
        self.stickers = new_stickers
    
    def is_solved(self) -> bool:
        """Check if the cube is in a solved state."""
        # Check each face has uniform color
        face_starts = [0, 9, 18, 27, 36, 45]
        for start in face_starts:
            face_color = self.stickers[start]
            for i in range(9):
                if self.stickers[start + i] != face_color:
                    return False
        return True
    
    def copy(self) -> 'CubeState':
        """Create a deep copy of the cube state."""
        new_cube = CubeState()
        new_cube.stickers = self.stickers.copy()
        return new_cube
    
    def __eq__(self, other) -> bool:
        """Check equality of two cube states."""
        if not isinstance(other, CubeState):
            return False
        return self.stickers == other.stickers

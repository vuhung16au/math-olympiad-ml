"""Group theory permutations for Rubik's Cube moves.

This module defines all basic moves as permutations of the 54 stickers.
Each move is represented as a permutation function that transforms sticker positions.
"""

from typing import List
from .cube_state import CubeState


def identity_permutation() -> List[int]:
    """Return identity permutation (no change)."""
    return list(range(54))


def rotate_face_clockwise(face_start: int) -> List[int]:
    """Generate permutation for rotating a face clockwise.
    
    Args:
        face_start: Starting index of the face (0, 9, 18, 27, 36, or 45)
    
    Returns:
        Permutation list for rotating just the face
    """
    perm = identity_permutation()
    # Face rotation: corners and edges cycle
    # 0->2, 2->8, 8->6, 6->0 (corners)
    # 1->5, 5->7, 7->3, 3->1 (edges)
    # 4 stays (center)
    corners = [(0, 2), (2, 8), (8, 6), (6, 0)]
    edges = [(1, 5), (5, 7), (7, 3), (3, 1)]
    
    for src, dst in corners:
        perm[face_start + dst] = face_start + src
    for src, dst in edges:
        perm[face_start + dst] = face_start + src
    
    return perm


def compose_permutations(p1: List[int], p2: List[int]) -> List[int]:
    """Compose two permutations: p1 after p2.
    
    Args:
        p1: First permutation
        p2: Second permutation
    
    Returns:
        Composition p1(p2(x))
    """
    return [p1[p2[i]] for i in range(54)]


def inverse_permutation(perm: List[int]) -> List[int]:
    """Get inverse of a permutation.
    
    Args:
        perm: Permutation to invert
    
    Returns:
        Inverse permutation
    """
    inv = [0] * 54
    for i in range(54):
        inv[perm[i]] = i
    return inv


# Move definitions
# Face indices: Top=0, Bottom=9, Front=18, Back=27, Left=36, Right=45

def move_U() -> List[int]:
    """U move: Rotate top face clockwise.
    
    Permutation: perm[i] = j means sticker at position i moves to position j.
    """
    perm = identity_permutation()
    
    # Rotate top face (0-8): 0->2, 2->8, 8->6, 6->0, 1->5, 5->7, 7->3, 3->1, 4->4
    perm[0] = 2
    perm[2] = 8
    perm[8] = 6
    perm[6] = 0
    perm[1] = 5
    perm[5] = 7
    perm[7] = 3
    perm[3] = 1
    # 4 stays at 4
    
    # Cycle top rows of adjacent faces
    # Need to read original positions first to avoid overwriting
    # Front top (18,19,20) -> Right top (45,46,47)
    # Right top (45,46,47) -> Back top (29,28,27) - reversed order
    # Back top (27,28,29) -> Left top (36,37,38) - reversed order  
    # Left top (36,37,38) -> Front top (18,19,20)
    
    # Store where each position should go (reading from identity)
    front_to_right = {18: 45, 19: 46, 20: 47}
    right_to_back = {45: 29, 46: 28, 47: 27}  # reversed
    back_to_left = {27: 36, 28: 37, 29: 38}  # reversed
    left_to_front = {36: 18, 37: 19, 38: 20}
    
    # Apply all mappings
    for src, dst in front_to_right.items():
        perm[src] = dst
    for src, dst in right_to_back.items():
        perm[src] = dst
    for src, dst in back_to_left.items():
        perm[src] = dst
    for src, dst in left_to_front.items():
        perm[src] = dst
    
    return perm


def move_U_prime() -> List[int]:
    """U' move: Rotate top face counter-clockwise."""
    return inverse_permutation(move_U())


def move_D() -> List[int]:
    """D move: Rotate bottom face clockwise."""
    perm = identity_permutation()
    
    # Rotate bottom face (9-17): 9->11, 11->17, 17->15, 15->9, 10->14, 14->16, 16->12, 12->10
    perm[9] = 11
    perm[11] = 17
    perm[17] = 15
    perm[15] = 9
    perm[10] = 14
    perm[14] = 16
    perm[16] = 12
    perm[12] = 10
    # 13 stays at 13
    
    # Cycle bottom rows of adjacent faces (opposite direction from U)
    # Front bottom (24,25,26) -> Left bottom (42,43,44)
    # Left bottom (42,43,44) -> Back bottom (35,34,33) - reversed
    # Back bottom (33,34,35) -> Right bottom (51,52,53) - reversed
    # Right bottom (51,52,53) -> Front bottom (24,25,26)
    
    perm[24] = 42
    perm[25] = 43
    perm[26] = 44
    perm[42] = 35
    perm[43] = 34
    perm[44] = 33
    perm[33] = 51
    perm[34] = 52
    perm[35] = 53
    perm[51] = 24
    perm[52] = 25
    perm[53] = 26
    
    return perm


def move_D_prime() -> List[int]:
    """D' move: Rotate bottom face counter-clockwise."""
    return inverse_permutation(move_D())


def move_R() -> List[int]:
    """R move: Rotate right face clockwise."""
    perm = identity_permutation()
    
    # Rotate right face (45-53): 45->47, 47->53, 53->51, 51->45, 46->50, 50->52, 52->48, 48->46
    perm[45] = 47
    perm[47] = 53
    perm[53] = 51
    perm[51] = 45
    perm[46] = 50
    perm[50] = 52
    perm[52] = 48
    perm[48] = 46
    # 49 stays at 49
    
    # Cycle right columns of adjacent faces
    # Top right column (2,5,8) -> Front right column (20,23,26)
    # Front right column (20,23,26) -> Bottom right column (11,14,17) - reversed
    # Bottom right column (11,14,17) -> Back left column (36,33,30) - reversed
    # Back left column (36,33,30) -> Top right column (2,5,8)
    
    # Top face right column: positions 2, 5, 8
    # Bottom face right column: positions 11, 14, 17 (bottom face indices 2,5,8 + 9)
    # Front face right column: positions 20, 23, 26 (front face indices 2,5,8 + 18)
    # Back face left column: positions 30, 33, 36 (back face indices 0,3,6 + 27, but reversed order)
    
    perm[2] = 20
    perm[5] = 23
    perm[8] = 26
    perm[20] = 11  # Bottom right
    perm[23] = 14
    perm[26] = 17
    perm[11] = 36  # Back left, reversed
    perm[14] = 33
    perm[17] = 30
    perm[36] = 2
    perm[33] = 5
    perm[30] = 8
    
    return perm


def move_R_prime() -> List[int]:
    """R' move: Rotate right face counter-clockwise."""
    return inverse_permutation(move_R())


def move_L() -> List[int]:
    """L move: Rotate left face clockwise."""
    perm = identity_permutation()
    
    # Rotate left face (36-44): 36->38, 38->44, 44->42, 42->36, 37->41, 41->43, 43->39, 39->37
    perm[36] = 38
    perm[38] = 44
    perm[44] = 42
    perm[42] = 36
    perm[37] = 41
    perm[41] = 43
    perm[43] = 39
    perm[39] = 37
    # 40 stays at 40
    
    # Cycle left columns (opposite from R)
    # Top left (0,3,6) -> Back right (38,35,32) - reversed
    # Back right (38,35,32) -> Bottom left (9,12,15) - reversed
    # Bottom left (9,12,15) -> Front left (18,21,24)
    # Front left (18,21,24) -> Top left (0,3,6)
    
    # Note: Back face right column indices are 38, 35, 32 (positions 2,5,8 in back face + 27)
    # But wait, back face indices: 27-35, so right column would be 29,32,35 (positions 2,5,8 + 27)
    # Actually, let me recalculate: back face is 27-35, right column in 3x3 is positions 2,5,8
    # So back right column = 27+2=29, 27+5=32, 27+8=35
    
    # Top left (0,3,6) -> Back right (29,32,35) - but we need to reverse the order
    # Back right (29,32,35) -> Bottom left (9,12,15) - reversed
    # Bottom left (9,12,15) -> Front left (18,21,24)
    # Front left (18,21,24) -> Top left (0,3,6)
    
    perm[0] = 35  # Top left -> Back right (reversed: 6->35)
    perm[3] = 32  # Top left -> Back right (reversed: 3->32)
    perm[6] = 29  # Top left -> Back right (reversed: 0->29)
    perm[29] = 9  # Back right -> Bottom left (reversed: 35->9)
    perm[32] = 12 # Back right -> Bottom left (reversed: 32->12)
    perm[35] = 15 # Back right -> Bottom left (reversed: 29->15)
    perm[9] = 18  # Bottom left -> Front left
    perm[12] = 21 # Bottom left -> Front left
    perm[15] = 24 # Bottom left -> Front left
    perm[18] = 0  # Front left -> Top left
    perm[21] = 3  # Front left -> Top left
    perm[24] = 6  # Front left -> Top left
    
    return perm


def move_L_prime() -> List[int]:
    """L' move: Rotate left face counter-clockwise."""
    return inverse_permutation(move_L())


def move_F() -> List[int]:
    """F move: Rotate front face clockwise."""
    perm = identity_permutation()
    
    # Rotate front face (18-26): 18->20, 20->26, 26->24, 24->18, 19->23, 23->25, 25->21, 21->19
    perm[18] = 20
    perm[20] = 26
    perm[26] = 24
    perm[24] = 18
    perm[19] = 23
    perm[23] = 25
    perm[25] = 21
    perm[21] = 19
    # 22 stays at 22
    
    # Cycle front edges
    # Top bottom row (6,7,8) -> Right left column (45,48,51)
    # Right left column (45,48,51) -> Bottom top row (9,10,11) - reversed
    # Bottom top row (9,10,11) -> Left right column (44,41,38) - reversed
    # Left right column (44,41,38) -> Top bottom row (6,7,8)
    
    perm[6] = 45
    perm[7] = 48
    perm[8] = 51
    perm[45] = 9
    perm[48] = 10
    perm[51] = 11
    perm[9] = 44
    perm[10] = 41
    perm[11] = 38
    perm[44] = 6
    perm[41] = 7
    perm[38] = 8
    
    return perm


def move_F_prime() -> List[int]:
    """F' move: Rotate front face counter-clockwise."""
    return inverse_permutation(move_F())


def move_B() -> List[int]:
    """B move: Rotate back face clockwise."""
    perm = identity_permutation()
    
    # Rotate back face (27-35): 27->29, 29->35, 35->33, 33->27, 28->32, 32->34, 34->30, 30->28
    perm[27] = 29
    perm[29] = 35
    perm[35] = 33
    perm[33] = 27
    perm[28] = 32
    perm[32] = 34
    perm[34] = 30
    perm[30] = 28
    # 31 stays at 31
    
    # Cycle back edges (opposite from F)
    # Top top row (0,1,2) -> Left left column (36,39,42)
    # Left left column (36,39,42) -> Bottom bottom row (15,16,17) - reversed
    # Bottom bottom row (15,16,17) -> Right right column (53,50,47) - reversed
    # Right right column (53,50,47) -> Top top row (0,1,2)
    
    perm[0] = 36
    perm[1] = 39
    perm[2] = 42
    perm[36] = 15
    perm[39] = 16
    perm[42] = 17
    perm[15] = 53
    perm[16] = 50
    perm[17] = 47
    perm[53] = 0
    perm[50] = 1
    perm[47] = 2
    
    return perm


def move_B_prime() -> List[int]:
    """B' move: Rotate back face counter-clockwise."""
    return inverse_permutation(move_B())


# Move dictionary for easy access
MOVES = {
    'U': move_U,
    "U'": move_U_prime,
    'D': move_D,
    "D'": move_D_prime,
    'R': move_R,
    "R'": move_R_prime,
    'L': move_L,
    "L'": move_L_prime,
    'F': move_F,
    "F'": move_F_prime,
    'B': move_B,
    "B'": move_B_prime,
}


def apply_move(cube: CubeState, move_name: str):
    """Apply a move to a cube state.
    
    Args:
        cube: CubeState to modify
        move_name: Name of the move (e.g., 'U', "U'", 'R', etc.)
    """
    if move_name not in MOVES:
        raise ValueError(f"Unknown move: {move_name}")
    
    perm = MOVES[move_name]()
    cube.apply_permutation(perm)


def apply_move_sequence(cube: CubeState, moves: List[str]):
    """Apply a sequence of moves to a cube state.
    
    Args:
        cube: CubeState to modify
        moves: List of move names
    """
    for move in moves:
        apply_move(cube, move)

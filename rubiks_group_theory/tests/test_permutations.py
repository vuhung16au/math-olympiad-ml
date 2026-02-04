from core.cube_state import CubeState
from core.permutations import (
    MOVES,
    apply_move,
    compose_permutations,
    identity_permutation,
    inverse_permutation,
)


def inverse_move(move: str) -> str:
    return move[:-1] if move.endswith("'") else f"{move}'"


def test_all_moves_are_valid_bijections():
    expected = set(range(54))
    for name, fn in MOVES.items():
        perm = fn()
        assert len(perm) == 54, f"{name} must map 54 stickers"
        assert set(perm) == expected, f"{name} must be a bijection"


def test_inverse_permutation_composes_to_identity():
    ident = identity_permutation()
    for name, fn in MOVES.items():
        perm = fn()
        inv = inverse_permutation(perm)
        assert compose_permutations(perm, inv) == ident, f"{name} * inv != I"
        assert compose_permutations(inv, perm) == ident, f"inv * {name} != I"


def test_move_then_inverse_returns_solved_state():
    for move in MOVES:
        cube = CubeState()
        apply_move(cube, move)
        apply_move(cube, inverse_move(move))
        assert cube.is_solved(), f"{move} followed by inverse should solve"


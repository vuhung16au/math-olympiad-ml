from core.cube_state import CubeState
from core.permutations import apply_move, apply_move_sequence
from solvers.two_phase_solver import TwoPhaseSolver


def inverse_move(move: str) -> str:
    return move[:-1] if move.endswith("'") else f"{move}'"


def test_reverse_sequence_solver_logic_solves_scramble():
    scramble = ["R", "U", "R'", "U'", "F", "D", "L", "B'", "U", "R"]
    cube = CubeState()
    apply_move_sequence(cube, scramble)
    assert not cube.is_solved()

    reverse_solution = [inverse_move(m) for m in reversed(scramble)]
    apply_move_sequence(cube, reverse_solution)
    assert cube.is_solved()


def test_two_phase_facelet_mapping_for_solved_cube():
    solver = TwoPhaseSolver()
    facelets = solver._to_kociemba_facelets(CubeState())  # deterministic mapping test
    assert facelets == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"


def test_two_phase_half_turn_expansion():
    solver = TwoPhaseSolver()
    expanded = solver._expand_half_turns("R2 U F2 B'")
    assert expanded == ["R", "R", "U", "F", "F", "B'"]


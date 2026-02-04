"""Move metrics and comparison helpers."""

from typing import Dict, List, Optional, Tuple


def parse_move_amount(move: str) -> Tuple[str, int]:
    """Convert move token to (face, quarter-turn amount mod 4)."""
    if move.endswith("2"):
        return move[0], 2
    if move.endswith("'"):
        return move[0], 3
    return move[0], 1


def canonicalize_moves(moves: List[str]) -> List[str]:
    """Reduce adjacent same-face moves for HTM/QTM counting."""
    reduced: List[Tuple[str, int]] = []
    for move in moves:
        face, amt = parse_move_amount(move)
        if reduced and reduced[-1][0] == face:
            prev_face, prev_amt = reduced[-1]
            new_amt = (prev_amt + amt) % 4
            if new_amt == 0:
                reduced.pop()
            else:
                reduced[-1] = (prev_face, new_amt)
        else:
            reduced.append((face, amt % 4))

    out = []
    for face, amt in reduced:
        if amt == 1:
            out.append(face)
        elif amt == 2:
            out.append(f"{face}2")
        elif amt == 3:
            out.append(f"{face}'")
    return out


def compute_move_metrics(moves: List[str]) -> Dict[str, int]:
    """Return HTM/QTM counts for a sequence."""
    canonical = canonicalize_moves(moves)
    htm = len(canonical)
    qtm = sum(2 if token.endswith("2") else 1 for token in canonical)
    return {"htm": htm, "qtm": qtm}


def build_compare_report(
    reverse_moves: List[str], two_phase_moves: Optional[List[str]]
) -> Dict[str, Optional[Dict[str, int]]]:
    """Build side-by-side move metric comparison."""
    reverse_metrics = compute_move_metrics(reverse_moves)
    report: Dict[str, Optional[Dict[str, int]]] = {
        "reverse": reverse_metrics,
        "two_phase": None,
        "delta_qtm": None,
        "delta_htm": None,
    }
    if two_phase_moves is not None:
        two_phase_metrics = compute_move_metrics(two_phase_moves)
        report["two_phase"] = two_phase_metrics
        report["delta_qtm"] = two_phase_metrics["qtm"] - reverse_metrics["qtm"]  # type: ignore[index]
        report["delta_htm"] = two_phase_metrics["htm"] - reverse_metrics["htm"]  # type: ignore[index]
    return report


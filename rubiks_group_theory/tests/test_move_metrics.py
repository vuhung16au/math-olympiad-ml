from core.move_metrics import (
    build_compare_report,
    canonicalize_moves,
    compute_move_metrics,
)


def test_canonicalize_adjacent_same_face():
    assert canonicalize_moves(["R", "R"]) == ["R2"]
    assert canonicalize_moves(["R", "R", "R"]) == ["R'"]
    assert canonicalize_moves(["R", "R", "R", "R"]) == []
    assert canonicalize_moves(["R", "U", "R"]) == ["R", "U", "R"]


def test_compute_move_metrics_counts_htm_and_qtm():
    # R R -> R2: HTM=1, QTM=2
    metrics = compute_move_metrics(["R", "R"])
    assert metrics["htm"] == 1
    assert metrics["qtm"] == 2

    # R2 U R' -> HTM=3, QTM=4
    metrics = compute_move_metrics(["R2", "U", "R'"])
    assert metrics["htm"] == 3
    assert metrics["qtm"] == 4


def test_build_compare_report_deltas():
    report = build_compare_report(
        reverse_moves=["R", "R", "U", "U"],  # canonical -> R2 U2 => QTM 4
        two_phase_moves=["R2", "U"],         # QTM 3
    )
    assert report["reverse"]["qtm"] == 4
    assert report["two_phase"]["qtm"] == 3
    assert report["delta_qtm"] == -1


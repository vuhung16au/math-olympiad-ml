"""Queue control state helpers."""

from typing import Dict


def compute_queue_button_states(solving: bool, animating: bool, paused: bool) -> Dict[str, bool]:
    """Compute enabled/disabled flags for pause/step/cancel buttons."""
    active = solving or animating
    return {
        "pause_enabled": active,
        "step_enabled": solving and paused,
        "cancel_enabled": active,
    }


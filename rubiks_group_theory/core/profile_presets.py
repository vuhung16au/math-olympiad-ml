"""Profile preset helpers for UI/animation tuning."""

from typing import Dict


def get_profile_settings(mode: str) -> Dict[str, object]:
    """Return timing/UI settings for the given profile mode."""
    if mode == "speed":
        return {
            "animation_duration_ms": 120,
            "solution_delay": 120,
            "overlay_duration": 300,
            "compact_ui": True,
            "show_explanations": False,
            "button_text": "Profile: SPD",
            "label": "Speed",
        }
    return {
        "animation_duration_ms": 320,
        "solution_delay": 650,
        "overlay_duration": 1000,
        "compact_ui": False,
        "show_explanations": True,
        "button_text": "Profile: Teach",
        "label": "Teaching",
    }


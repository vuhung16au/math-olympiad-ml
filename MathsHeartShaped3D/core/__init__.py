"""
Core modules for heart animation generation.
"""

from .heart_generator import generate_heart_points
from .figure_setup import setup_figure
from .audio_sync import (
    get_beat_intensity,
    get_onset_intensity,
    get_loudness_at_time,
    get_bass_at_time,
    get_tempo_at_time
)

__all__ = [
    'generate_heart_points',
    'setup_figure',
    'get_beat_intensity',
    'get_onset_intensity',
    'get_loudness_at_time',
    'get_bass_at_time',
    'get_tempo_at_time'
]


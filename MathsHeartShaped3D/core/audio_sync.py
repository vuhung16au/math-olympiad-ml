"""
Audio synchronization helper functions for effects.
"""

import numpy as np


def get_beat_intensity(current_time, beat_times, window=0.1):
    """
    Check if there's a beat near current_time.
    Returns intensity (0-1) based on proximity to nearest beat.
    
    Parameters:
    - current_time: Current time in seconds
    - beat_times: List of beat timestamps
    - window: Time window in seconds to consider a beat active
    
    Returns:
    - float: Intensity (0-1) where 1.0 is exactly on beat
    """
    if not beat_times or len(beat_times) == 0:
        return 0.0
    
    # Find nearest beat
    distances = np.abs(np.array(beat_times) - current_time)
    nearest_idx = np.argmin(distances)
    nearest_distance = distances[nearest_idx]
    
    # If within window, return intensity (closer = stronger)
    if nearest_distance < window:
        intensity = 1.0 - (nearest_distance / window)
        return float(intensity)
    return 0.0


def get_onset_intensity(current_time, onset_times, window=0.15):
    """
    Check if there's an onset near current_time.
    
    Parameters:
    - current_time: Current time in seconds
    - onset_times: List of onset timestamps
    - window: Time window in seconds to consider an onset active
    
    Returns:
    - float: Intensity (0-1) where 1.0 is exactly on onset
    """
    if not onset_times or len(onset_times) == 0:
        return 0.0
    
    distances = np.abs(np.array(onset_times) - current_time)
    nearest_distance = np.min(distances)
    
    if nearest_distance < window:
        intensity = 1.0 - (nearest_distance / window)
        return float(intensity)
    return 0.0


def get_loudness_at_time(current_time, rms_times, rms_values):
    """
    Get normalized loudness (0-1) at current_time.
    
    Parameters:
    - current_time: Current time in seconds
    - rms_times: List of RMS measurement timestamps
    - rms_values: List of normalized RMS values (0-1)
    
    Returns:
    - float: Normalized loudness (0-1)
    """
    if not rms_times or not rms_values or len(rms_times) == 0:
        return 0.5
    
    # Find nearest RMS measurement
    distances = np.abs(np.array(rms_times) - current_time)
    idx = np.argmin(distances)
    return float(rms_values[idx])


def get_bass_at_time(current_time, bass_times, bass_values):
    """
    Get bass strength (0-1) at current_time.
    
    Parameters:
    - current_time: Current time in seconds
    - bass_times: List of bass measurement timestamps
    - bass_values: List of normalized bass strength values (0-1)
    
    Returns:
    - float: Normalized bass strength (0-1)
    """
    if not bass_times or not bass_values or len(bass_times) == 0:
        return 0.5
    
    distances = np.abs(np.array(bass_times) - current_time)
    idx = np.argmin(distances)
    return float(bass_values[idx])


def get_tempo_at_time(current_time, tempo_times, tempo_values):
    """
    Get tempo (BPM) at current_time.
    
    Parameters:
    - current_time: Current time in seconds
    - tempo_times: List of tempo measurement timestamps
    - tempo_values: List of BPM values
    
    Returns:
    - float: Tempo in BPM
    """
    if not tempo_times or not tempo_values or len(tempo_times) == 0:
        return 120.0  # Default
    
    distances = np.abs(np.array(tempo_times) - current_time)
    idx = np.argmin(distances)
    return float(tempo_values[idx])


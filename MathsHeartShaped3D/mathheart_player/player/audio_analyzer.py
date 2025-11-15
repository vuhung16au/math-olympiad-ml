"""
Audio Analyzer Module for MathHeart Player
Hybrid approach: pre-analyze (with caching) + streaming fallback
"""

import os
import sys
import librosa
import numpy as np
from typing import Optional, Dict, Callable

# Add parent directory to path to import existing modules
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from analyze_audio import analyze_audio
from core.audio_sync import (
    get_beat_intensity,
    get_onset_intensity,
    get_loudness_at_time,
    get_bass_at_time,
    get_tempo_at_time
)
from mathheart_player.player.analysis_cache import load_from_cache, save_to_cache


class AudioAnalyzer:
    """Hybrid audio analyzer with pre-analysis (cached) and streaming fallback."""
    
    def __init__(self, progress_callback: Optional[Callable[[str, float], None]] = None):
        """
        Initialize audio analyzer.
        
        Parameters:
            progress_callback: Optional callback for analysis progress (message, progress)
        """
        self.current_file: Optional[str] = None
        self.features: Optional[Dict] = None
        self.audio_data: Optional[np.ndarray] = None
        self.sample_rate: int = 22050
        self.progress_callback = progress_callback
        
    def load_file(self, filepath: str, use_cache: bool = True) -> bool:
        """
        Load and analyze audio file.
        
        Parameters:
            filepath: Path to audio file
            use_cache: Whether to use cache for pre-analyzed features
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(filepath):
            return False
        
        self.current_file = filepath
        
        # Try to load from cache first
        if use_cache:
            cached_features = load_from_cache(filepath)
            if cached_features:
                self.features = cached_features
                if self.progress_callback:
                    self.progress_callback("Loaded from cache", 1.0)
                return True
        
        # Cache miss - run full analysis
        if self.progress_callback:
            self.progress_callback("Analyzing audio...", 0.0)
        
        try:
            # Use existing analyze_audio function
            # Create temporary output path
            import tempfile
            temp_output = os.path.join(
                tempfile.gettempdir(),
                f"mathheart_temp_{os.getpid()}.json"
            )
            
            # Run analysis (this will show progress with tqdm)
            # Note: tqdm progress bars work fine in background threads
            # as long as we're using the callback for UI updates
            self.features = analyze_audio(filepath, temp_output)
            
            # Save to cache
            if use_cache:
                save_to_cache(filepath, self.features)
            
            # Clean up temp file
            if os.path.exists(temp_output):
                try:
                    os.remove(temp_output)
                except:
                    pass
            
            if self.progress_callback:
                self.progress_callback("Analysis complete", 1.0)
            
            return True
        except Exception as e:
            print(f"Error analyzing audio: {e}")
            if self.progress_callback:
                self.progress_callback(f"Analysis failed: {e}", 0.0)
            return False
    
    def get_features_at_time(self, current_time: float) -> Dict[str, float]:
        """
        Get audio features at current playback time.
        Uses pre-analyzed data (primary) with streaming fallback if needed.
        
        Parameters:
            current_time: Current playback time in seconds
            
        Returns:
            Dictionary with audio features:
            - beat_intensity: 0-1
            - onset_intensity: 0-1
            - loudness: 0-1
            - bass: 0-1
            - tempo: BPM
        """
        if self.features is None:
            # No features available - return defaults
            return {
                'beat_intensity': 0.0,
                'onset_intensity': 0.0,
                'loudness': 0.5,
                'bass': 0.5,
                'tempo': 120.0
            }
        
        # Extract feature arrays
        beat_times = self.features.get('beat_times', [])
        onset_times = self.features.get('onset_times', [])
        rms_times = self.features.get('rms_times', [])
        rms_values = self.features.get('rms_values', [])
        bass_times = self.features.get('bass_times', [])
        bass_values = self.features.get('bass_values', [])
        tempo_times = self.features.get('tempo_times', [])
        tempo_values = self.features.get('tempo_values', [])
        
        # Query features using existing functions
        beat_intensity = get_beat_intensity(current_time, beat_times, window=0.1)
        onset_intensity = get_onset_intensity(current_time, onset_times, window=0.15)
        loudness = get_loudness_at_time(current_time, rms_times, rms_values)
        bass = get_bass_at_time(current_time, bass_times, bass_values)
        tempo = get_tempo_at_time(current_time, tempo_times, tempo_values)
        
        return {
            'beat_intensity': beat_intensity,
            'onset_intensity': onset_intensity,
            'loudness': loudness,
            'bass': bass,
            'tempo': tempo
        }
    
    def get_duration(self) -> float:
        """
        Get audio duration in seconds.
        
        Returns:
            Duration in seconds, or 0.0 if not loaded
        """
        if self.features:
            return self.features.get('duration', 0.0)
        return 0.0
    
    def get_all_features(self) -> Optional[Dict]:
        """
        Get all pre-analyzed features.
        
        Returns:
            Dictionary with all features, or None if not loaded
        """
        return self.features
    
    def clear(self):
        """Clear current analysis data."""
        self.current_file = None
        self.features = None
        self.audio_data = None


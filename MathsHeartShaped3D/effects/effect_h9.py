"""
Effect H9: "Cuba to New Orleans" - A Musical Journey Through the Heart
Real-time audio-synchronized animation with strategic through-heart passages
"""

import numpy as np
from effects import BaseEffect, register_effect
from core.audio_sync import (
    get_beat_intensity,
    get_onset_intensity,
    get_loudness_at_time,
    get_bass_at_time,
    get_tempo_at_time
)


class EffectH9(BaseEffect):
    """Cuba to New Orleans: Musical Journey Through the Heart with Through-Heart Passages."""
    
    def get_total_frames(self):
        # Audio duration: 697.90 seconds at 30 fps
        return int(697.90 * 30)  # 20937 frames
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        total_duration = 697.90
        
        # Load audio features if available
        if self.audio_features:
            beat_times = self.audio_features.get('beat_times', [])
            onset_times = self.audio_features.get('onset_times', [])
            rms_times = self.audio_features.get('rms_times', [])
            rms_values = self.audio_features.get('rms_values', [])
            bass_times = self.audio_features.get('bass_times', [])
            bass_values = self.audio_features.get('bass_values', [])
            tempo_times = self.audio_features.get('tempo_times', [])
            tempo_values = self.audio_features.get('tempo_values', [])
            
            # Get current audio features
            beat_intensity = get_beat_intensity(current_second, beat_times, window=0.1)
            onset_intensity = get_onset_intensity(current_second, onset_times, window=0.15)
            loudness = get_loudness_at_time(current_second, rms_times, rms_values)
            bass = get_bass_at_time(current_second, bass_times, bass_values)
            current_tempo = get_tempo_at_time(current_second, tempo_times, tempo_values)
        else:
            # Fallback to hardcoded values if no audio features
            beat_intensity = 0.0
            onset_intensity = 0.0
            loudness = 0.5
            bass = 0.5
            current_tempo = 75.0
        
        # Heart rotates 360+ degrees over full duration, tempo-adaptive
        tempo_factor = current_tempo / 75.0  # Normalize to 75 BPM baseline
        alpha_deg = frame * 360 * tempo_factor / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_base = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_base = self.y_original
        z_base = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Heartbeat pulse synchronized with beats
        heartbeat_scale = 1.0
        if beat_intensity > 0:
            heartbeat_scale = 1.0 + 0.2 * beat_intensity
        
        if onset_intensity > 0.5:
            heartbeat_scale = max(heartbeat_scale, 1.0 + 0.15 * onset_intensity)
        
        # Apply heartbeat
        x_rotated = x_base * heartbeat_scale
        y_rotated = y_base * heartbeat_scale
        z_rotated = z_base * heartbeat_scale
        
        point_alpha = 0.8
        
        # Phase 1 (0-30s): Opening - Heart emerges from silence (Cuba introduction)
        if current_second < 30.0:
            phase_t = current_second / 30.0
            point_alpha = 0.8 * phase_t
            scale = 0.1 + 0.9 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
            base_zoom = 200 - 150 * phase_t
            zoom_factor = base_zoom - 10 * loudness
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 90 * phase_t
        
        # Phase 2 (30-100s): Cuban rhythms build
        elif current_second < 100.0:
            phase_t = (current_second - 30.0) / 70.0
            point_alpha = 0.6 + 0.2 * bass + 0.2 * phase_t
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 50 - 20 * phase_t
            zoom_factor = base_zoom - 8 * loudness
            elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 135 + 180 * phase_t
        
        # Phase 3 (100-120s): FIRST THROUGH-HEART PASSAGE - Transition to New Orleans
        elif current_second < 120.0:
            phase_t = (current_second - 100.0) / 20.0
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Dramatic zoom through heart: 30 → -15
            zoom_factor = 30 - 45 * (phase_t ** 1.5)
            elevation = 20 + 20 * np.sin(np.pi * phase_t)
            azimuth = 315 + 90 * phase_t
        
        # Phase 4 (120-140s): Exit and recovery from first passage
        elif current_second < 140.0:
            phase_t = (current_second - 120.0) / 20.0
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -15 → 40
            zoom_factor = -15 + 55 * phase_t
            elevation = 40 - 20 * phase_t
            azimuth = 405 + 90 * phase_t
        
        # Phase 5 (140-250s): New Orleans soul emerges
        elif current_second < 250.0:
            phase_t = (current_second - 140.0) / 110.0
            point_alpha = 0.7 + 0.3 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 40 - 10 * phase_t
            zoom_factor = base_zoom - 8 * loudness
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 495 + 270 * phase_t
        
        # Phase 6 (250-270s): SECOND THROUGH-HEART PASSAGE - Musical climax
        elif current_second < 270.0:
            phase_t = (current_second - 250.0) / 20.0
            point_alpha = 0.9 + 0.1 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Dramatic zoom through heart: 30 → -20
            zoom_factor = 30 - 50 * (phase_t ** 2)
            elevation = 15 + 25 * np.sin(np.pi * phase_t)
            azimuth = 765 + 180 * phase_t
        
        # Phase 7 (270-290s): Exit and turnaround
        elif current_second < 290.0:
            phase_t = (current_second - 270.0) / 20.0
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -20 → 50
            zoom_factor = -20 + 70 * phase_t
            elevation = 40 - 15 * phase_t
            azimuth = 945 + 90 * phase_t
        
        # Phase 8 (290-450s): Fusion - Cuba meets New Orleans
        elif current_second < 450.0:
            phase_t = (current_second - 290.0) / 160.0
            point_alpha = 0.6 + 0.4 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 50 + 30 * np.sin(4 * np.pi * phase_t)
            zoom_factor = base_zoom - 10 * loudness
            elevation = 20 + 25 * np.sin(3 * np.pi * phase_t)
            azimuth = 1035 + 360 * phase_t
        
        # Phase 9 (450-470s): THIRD THROUGH-HEART PASSAGE - Peak intensity
        elif current_second < 470.0:
            phase_t = (current_second - 450.0) / 20.0
            point_alpha = 1.0  # Maximum brightness
            # Most dramatic passage: 40 → -25
            zoom_factor = 40 - 65 * (phase_t ** 1.8)
            elevation = 10 + 30 * np.sin(np.pi * phase_t)
            azimuth = 1395 + 270 * phase_t
        
        # Phase 10 (470-490s): Exit from peak
        elif current_second < 490.0:
            phase_t = (current_second - 470.0) / 20.0
            point_alpha = 0.9 + 0.1 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -25 → 60
            zoom_factor = -25 + 85 * phase_t
            elevation = 40 - 20 * phase_t
            azimuth = 1665 + 90 * phase_t
        
        # Phase 11 (490-600s): Resolution and reflection
        elif current_second < 600.0:
            phase_t = (current_second - 490.0) / 110.0
            point_alpha = 0.7 + 0.3 * bass * (1.0 - 0.3 * phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 60 + 40 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
            azimuth = 1755 + 180 * phase_t
        
        # Phase 12 (600-620s): FOURTH THROUGH-HEART PASSAGE - Final transformation
        elif current_second < 620.0:
            phase_t = (current_second - 600.0) / 20.0
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Final passage: 100 → -10
            zoom_factor = 100 - 110 * (phase_t ** 1.5)
            elevation = 20 + 20 * np.sin(np.pi * phase_t)
            azimuth = 1935 + 180 * phase_t
        
        # Phase 13 (620-650s): Final exit and preparation for ending
        elif current_second < 650.0:
            phase_t = (current_second - 620.0) / 30.0
            point_alpha = 0.7 + 0.3 * bass * (1.0 - phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -10 → 80
            zoom_factor = -10 + 90 * phase_t
            elevation = 40 - 20 * phase_t
            azimuth = 2115 + 90 * phase_t
        
        # Phase 14 (650-697.9s): Fade to silence - Journey complete
        else:
            phase_t = (current_second - 650.0) / 47.9
            point_alpha = (0.7 + 0.3 * bass) * (1.0 - phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 80 + 120 * phase_t
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20
            azimuth = 2205 + 90 * phase_t
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H9', EffectH9)


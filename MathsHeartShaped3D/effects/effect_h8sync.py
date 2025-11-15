"""
Effect H8sync: Heart Genesis with Real Audio Sync (using librosa-detected features - 100 seconds)
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


class EffectH8sync(BaseEffect):
    """Heart Genesis with Real Audio Sync: using librosa-detected features."""
    
    def get_total_frames(self):
        return 3000  # 100 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
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
        
        # Heart rotates slowly (180 degrees total, tempo-adjusted)
        # Adjust rotation speed based on tempo (faster tempo = faster rotation)
        tempo_factor = current_tempo / 75.0  # Normalize to 75 BPM baseline
        alpha_deg = frame * 180 * tempo_factor / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_base = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_base = self.y_original
        z_base = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Heartbeat pulse synchronized with beats
        heartbeat_scale = 1.0
        if beat_intensity > 0:
            # Pulse on beat: stronger beat = bigger pulse
            heartbeat_scale = 1.0 + 0.2 * beat_intensity
        
        # Also pulse on strong onsets
        if onset_intensity > 0.5:
            heartbeat_scale = max(heartbeat_scale, 1.0 + 0.15 * onset_intensity)
        
        # Apply heartbeat
        x_rotated = x_base * heartbeat_scale
        y_rotated = y_base * heartbeat_scale
        z_rotated = z_base * heartbeat_scale
        
        point_alpha = 0.8
        
        # Phase 1 (0-10s): Empty black space, then gradually heart appears
        if current_second < 10.0:
            phase_t = current_second / 10.0
            # Gradually fade in from blank
            point_alpha = 0.8 * phase_t
            # Scale from very small to normal
            scale = 0.1 + 0.9 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
            # Adjust zoom based on loudness (louder = closer)
            base_zoom = 200 - 175 * phase_t
            zoom_factor = base_zoom - 5 * loudness  # Louder = zoom in more
            elevation = 20
            azimuth = 45
        
        # Phase 2 (10-25s): Energy burst, strings ascending
        elif current_second < 25.0:
            phase_t = (current_second - 10.0) / 15.0
            point_alpha = 0.8
            # Zoom based on loudness
            base_zoom = 25 - 5 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20
            azimuth = 45 + 90 * phase_t
        
        # Phase 3 (25-40s): Strings coalesce
        elif current_second < 40.0:
            phase_t = (current_second - 25.0) / 15.0
            point_alpha = 0.8
            base_zoom = 20 - 3 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20 + 10 * np.sin(np.pi * phase_t)
            azimuth = 135 + 90 * phase_t
        
        # Phase 4 (40-60s): Heartbeat rhythm
        elif current_second < 60.0:
            phase_t = (current_second - 40.0) / 20.0
            point_alpha = 0.8
            # Zoom based on loudness
            zoom_factor = 17 - 5 * loudness
            elevation = 20
            azimuth = 225 + 180 * phase_t
        
        # Phase 5 (60-75s): Majestic orchestral
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 0.8
            base_zoom = 17 + 3 * np.sin(2 * np.pi * phase_t)
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 405 + 360 * phase_t
        
        # Phase 6 (75-90s): Cosmic expansion
        elif current_second < 90.0:
            phase_t = (current_second - 75.0) / 15.0
            # Adjust alpha based on bass (more bass = brighter)
            point_alpha = 0.6 + 0.4 * bass + 0.2 * phase_t  # Glow effect
            point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
            base_zoom = 20 + 80 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 40 - 20 * phase_t
            azimuth = 585 + 90 * phase_t
        
        # Phase 7 (90-95s): Mathematical precision
        elif current_second < 95.0:
            phase_t = (current_second - 90.0) / 5.0
            point_alpha = 0.6 + 0.4 * bass  # Fully bright based on bass
            point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
            zoom_factor = 100 - 5 * loudness
            elevation = 20
            azimuth = 675
        
        # Phase 8 (95-100s): Fade to silence, infinite stars
        else:
            phase_t = (current_second - 95.0) / 5.0
            point_alpha = (0.6 + 0.4 * bass) * (1.0 - phase_t)  # Fade out
            point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
            base_zoom = 100 + 100 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20
            azimuth = 675
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H8sync', EffectH8sync)


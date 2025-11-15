"""
Effect H10: The Mission (Gabriel's Oboe) - A Spiritual Journey Through the Heart
Real-time audio-synchronized animation with strategic through-heart passages
Improved zoom factors to keep heart visible throughout
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


class EffectH10(BaseEffect):
    """The Mission (Gabriel's Oboe): Spiritual Journey Through the Heart with Through-Heart Passages."""
    
    def get_total_frames(self):
        # Calculate duration from audio features if available, otherwise use default
        # Default: estimate 4 minutes (240 seconds) for classical piece
        if self.audio_features and 'rms_times' in self.audio_features:
            rms_times = self.audio_features.get('rms_times', [])
            if len(rms_times) > 0:
                duration = rms_times[-1]  # Last RMS timestamp approximates duration
                return int(duration * 30)  # 30 fps
        
        # Fallback: 240 seconds (4 minutes) at 30 fps
        return 7200  # 240 seconds * 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Calculate total duration from frames
        total_duration = self.total_frames / self.fps
        
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
            current_tempo = 60.0  # Slower for classical piece
        
        # Heart rotates 360+ degrees over full duration, tempo-adaptive (slower for classical)
        tempo_factor = current_tempo / 60.0  # Normalize to 60 BPM baseline (slower than H9)
        alpha_deg = frame * 360 * tempo_factor / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_base = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_base = self.y_original
        z_base = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Heartbeat pulse synchronized with beats (gentler for classical)
        heartbeat_scale = 1.0
        if beat_intensity > 0:
            heartbeat_scale = 1.0 + 0.15 * beat_intensity  # Gentler than H9
        
        if onset_intensity > 0.5:
            heartbeat_scale = max(heartbeat_scale, 1.0 + 0.1 * onset_intensity)
        
        # Apply heartbeat
        x_rotated = x_base * heartbeat_scale
        y_rotated = y_base * heartbeat_scale
        z_rotated = z_base * heartbeat_scale
        
        point_alpha = 0.8
        
        # Calculate phase boundaries as percentages of total duration
        phase1_end = total_duration * 0.08  # 8% - Opening
        phase2_end = total_duration * 0.20  # 12% - Oboe introduction
        phase3_end = total_duration * 0.25  # 5% - FIRST THROUGH-HEART PASSAGE
        phase4_end = total_duration * 0.28  # 3% - Exit and recovery
        phase5_end = total_duration * 0.45  # 17% - Orchestral development
        phase6_end = total_duration * 0.50  # 5% - SECOND THROUGH-HEART PASSAGE
        phase7_end = total_duration * 0.53  # 3% - Exit and recovery
        phase8_end = total_duration * 0.70  # 17% - Emotional peak
        phase9_end = total_duration * 0.75  # 5% - THIRD THROUGH-HEART PASSAGE
        phase10_end = total_duration * 0.78  # 3% - Exit and recovery
        phase11_end = total_duration * 0.90  # 12% - Resolution
        phase12_end = total_duration * 0.93  # 3% - FOURTH THROUGH-HEART PASSAGE (if needed)
        phase13_end = total_duration * 0.96  # 3% - Final exit
        # phase14: 96-100% - Fade to silence
        
        # Phase 1 (0-8%): Opening - Heart emerges from silence (oboe introduction)
        if current_second < phase1_end:
            phase_t = current_second / phase1_end
            point_alpha = 0.8 * phase_t
            scale = 0.1 + 0.9 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
            # Start far, zoom to comfortable viewing distance
            base_zoom = 100 - 75 * phase_t  # 100 → 25
            zoom_factor = base_zoom - 3 * loudness  # Reduced loudness impact
            elevation = 20 + 5 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 45 * phase_t
        
        # Phase 2 (8-20%): Oboe melody introduction - gentle, contemplative
        elif current_second < phase2_end:
            phase_t = (current_second - phase1_end) / (phase2_end - phase1_end)
            point_alpha = 0.7 + 0.1 * bass + 0.1 * phase_t
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Comfortable viewing distance with gentle variation
            base_zoom = 20 + 3 * np.sin(3 * np.pi * phase_t)  # 18-23 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20 + 8 * np.sin(2 * np.pi * phase_t)
            azimuth = 90 + 90 * phase_t
        
        # Phase 3 (20-25%): FIRST THROUGH-HEART PASSAGE - Oboe solo climax
        elif current_second < phase3_end:
            phase_t = (current_second - phase2_end) / (phase3_end - phase2_end)
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Start from closer distance: 30 → -15
            zoom_factor = 30 - 45 * (phase_t ** 1.5)
            elevation = 20 + 15 * np.sin(np.pi * phase_t)
            azimuth = 180 + 90 * phase_t
        
        # Phase 4 (25-28%): Exit and recovery from first passage
        elif current_second < phase4_end:
            phase_t = (current_second - phase3_end) / (phase4_end - phase3_end)
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -15 → 22 (closer recovery)
            zoom_factor = -15 + 37 * phase_t
            elevation = 35 - 10 * phase_t
            azimuth = 270 + 60 * phase_t
        
        # Phase 5 (28-45%): Orchestral development - flowing, contemplative
        elif current_second < phase5_end:
            phase_t = (current_second - phase4_end) / (phase5_end - phase4_end)
            point_alpha = 0.7 + 0.3 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Comfortable viewing with gentle movement
            base_zoom = 20 + 5 * np.sin(4 * np.pi * phase_t)  # 15-25 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20 + 12 * np.sin(3 * np.pi * phase_t)
            azimuth = 330 + 180 * phase_t
        
        # Phase 6 (45-50%): SECOND THROUGH-HEART PASSAGE - Orchestral swell
        elif current_second < phase6_end:
            phase_t = (current_second - phase5_end) / (phase6_end - phase5_end)
            point_alpha = 0.9 + 0.1 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Start from medium distance: 28 → -18
            zoom_factor = 28 - 46 * (phase_t ** 2)
            elevation = 18 + 20 * np.sin(np.pi * phase_t)
            azimuth = 510 + 120 * phase_t
        
        # Phase 7 (50-53%): Exit and recovery
        elif current_second < phase7_end:
            phase_t = (current_second - phase6_end) / (phase7_end - phase6_end)
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -18 → 25 (comfortable recovery)
            zoom_factor = -18 + 43 * phase_t
            elevation = 38 - 12 * phase_t
            azimuth = 630 + 60 * phase_t
        
        # Phase 8 (53-70%): Emotional peak - orchestral and oboe dialogue
        elif current_second < phase8_end:
            phase_t = (current_second - phase7_end) / (phase8_end - phase7_end)
            point_alpha = 0.6 + 0.4 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Intimate to medium distance with variation
            base_zoom = 18 + 7 * np.sin(5 * np.pi * phase_t)  # 11-25 range
            zoom_factor = base_zoom - 4 * loudness
            elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 690 + 270 * phase_t
        
        # Phase 9 (70-75%): THIRD THROUGH-HEART PASSAGE - Peak emotional moment
        elif current_second < phase9_end:
            phase_t = (current_second - phase8_end) / (phase9_end - phase8_end)
            point_alpha = 1.0  # Maximum brightness
            # Most dramatic passage: 25 → -20
            zoom_factor = 25 - 45 * (phase_t ** 1.8)
            elevation = 15 + 25 * np.sin(np.pi * phase_t)
            azimuth = 960 + 180 * phase_t
        
        # Phase 10 (75-78%): Exit from peak
        elif current_second < phase10_end:
            phase_t = (current_second - phase9_end) / (phase10_end - phase9_end)
            point_alpha = 0.9 + 0.1 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -20 → 22 (comfortable recovery)
            zoom_factor = -20 + 42 * phase_t
            elevation = 40 - 15 * phase_t
            azimuth = 1140 + 60 * phase_t
        
        # Phase 11 (78-90%): Resolution and reflection - gentle conclusion
        elif current_second < phase11_end:
            phase_t = (current_second - phase10_end) / (phase11_end - phase10_end)
            point_alpha = 0.7 + 0.3 * bass * (1.0 - 0.2 * phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Comfortable viewing, gradually pulling back slightly
            base_zoom = 22 + 8 * phase_t  # 22 → 30
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 1200 + 120 * phase_t
        
        # Phase 12 (90-93%): FOURTH THROUGH-HEART PASSAGE - Final transformation
        elif current_second < phase12_end:
            phase_t = (current_second - phase11_end) / (phase12_end - phase11_end)
            point_alpha = 0.8 + 0.2 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Final passage: 35 → -12
            zoom_factor = 35 - 47 * (phase_t ** 1.5)
            elevation = 20 + 18 * np.sin(np.pi * phase_t)
            azimuth = 1320 + 90 * phase_t
        
        # Phase 13 (93-96%): Final exit and preparation for ending
        elif current_second < phase13_end:
            phase_t = (current_second - phase12_end) / (phase13_end - phase12_end)
            point_alpha = 0.7 + 0.3 * bass * (1.0 - phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Exit: -12 → 30 (medium distance)
            zoom_factor = -12 + 42 * phase_t
            elevation = 38 - 18 * phase_t
            azimuth = 1410 + 60 * phase_t
        
        # Phase 14 (96-100%): Fade to silence - gentle resolution
        else:
            phase_t = (current_second - phase13_end) / (total_duration - phase13_end)
            point_alpha = (0.7 + 0.3 * bass) * (1.0 - phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Gentle fade-out zoom
            base_zoom = 30 + 70 * phase_t  # 30 → 100
            zoom_factor = base_zoom - 2 * loudness
            elevation = 20
            azimuth = 1470 + 90 * phase_t
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H10', EffectH10)


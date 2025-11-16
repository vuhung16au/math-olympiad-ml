"""
Effect I2: Five Hearts - Multi-heart visualization with comprehensive audio synchronization
1st heart: beats, 2nd heart: tempo, 3rd heart: loudness, 4th heart: bass, 5th heart: onsets
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


class EffectI2(BaseEffect):
    """Five Hearts: Multi-heart visualization with comprehensive audio feature synchronization."""
    
    def __init__(self, total_frames, fps, x_original, y_original, z_original, 
                 scatter, ax, audio_features=None, 
                 x_heart2=None, y_heart2=None, z_heart2=None, scatter2=None,
                 x_heart3=None, y_heart3=None, z_heart3=None, scatter3=None,
                 x_heart4=None, y_heart4=None, z_heart4=None, scatter4=None,
                 x_heart5=None, y_heart5=None, z_heart5=None, scatter5=None):
        """Initialize with additional heart coordinates and scatter plots."""
        super().__init__(total_frames, fps, x_original, y_original, z_original, 
                        scatter, ax, audio_features)
        # Heart 2 (tempo)
        self.x_heart2 = x_heart2 if x_heart2 is not None else x_original
        self.y_heart2 = y_heart2 if y_heart2 is not None else y_original
        self.z_heart2 = z_heart2 if z_heart2 is not None else z_original
        self.scatter2 = scatter2
        # Heart 3 (loudness)
        self.x_heart3 = x_heart3 if x_heart3 is not None else x_original
        self.y_heart3 = y_heart3 if y_heart3 is not None else y_original
        self.z_heart3 = z_heart3 if z_heart3 is not None else z_original
        self.scatter3 = scatter3
        # Heart 4 (bass)
        self.x_heart4 = x_heart4 if x_heart4 is not None else x_original
        self.y_heart4 = y_heart4 if y_heart4 is not None else y_original
        self.z_heart4 = z_heart4 if z_heart4 is not None else z_original
        self.scatter4 = scatter4
        # Heart 5 (onsets)
        self.x_heart5 = x_heart5 if x_heart5 is not None else x_original
        self.y_heart5 = y_heart5 if y_heart5 is not None else y_original
        self.z_heart5 = z_heart5 if z_heart5 is not None else z_original
        self.scatter5 = scatter5
    
    def get_total_frames(self):
        # Calculate duration from audio features if available, otherwise use default
        if self.audio_features and 'rms_times' in self.audio_features:
            rms_times = self.audio_features.get('rms_times', [])
            if len(rms_times) > 0:
                duration = rms_times[-1]  # Last RMS timestamp approximates duration
                return int(duration * self.fps)
        
        # Fallback: 60 seconds at 30 fps
        return 1800  # 60 seconds * 30 fps
    
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
            current_tempo = 75.0
        
        # Calculate phase boundaries as percentages of total duration
        phase1_end = total_duration * 0.10   # 0-10%: Opening - hearts appear sequentially
        phase2_end = total_duration * 0.25   # 10-25%: Establishment
        phase3_end = total_duration * 0.40   # 25-40%: Development
        phase4_end = total_duration * 0.60   # 40-60%: Harmony
        phase5_end = total_duration * 0.75   # 60-75%: Climax
        phase6_end = total_duration * 0.90   # 75-90%: Peak synchronization
        # phase7: 90-100% - Resolution
        
        # 1st Heart (Beats): Rotates based on tempo, pulses on beats
        tempo_factor = current_tempo / 60.0
        alpha1_deg = frame * 360 * tempo_factor / self.total_frames
        alpha1_rad = np.deg2rad(alpha1_deg)
        
        x1_base = self.x_original * np.cos(alpha1_rad) + self.z_original * np.sin(alpha1_rad)
        y1_base = self.y_original
        z1_base = -self.x_original * np.sin(alpha1_rad) + self.z_original * np.cos(alpha1_rad)
        
        heartbeat1_scale = 1.0
        if beat_intensity > 0:
            heartbeat1_scale = 1.0 + 0.2 * beat_intensity
        if onset_intensity > 0.5:
            heartbeat1_scale = max(heartbeat1_scale, 1.0 + 0.15 * onset_intensity)
        
        x1_final = x1_base * heartbeat1_scale
        y1_final = y1_base * heartbeat1_scale
        z1_final = z1_base * heartbeat1_scale
        
        # 2nd Heart (Tempo): Independent rotation, syncs with tempo
        alpha2_deg = frame * 360 * tempo_factor / self.total_frames * (-0.7)  # Counter-rotate
        alpha2_rad = np.deg2rad(alpha2_deg)
        
        x2_base = self.x_heart2 * np.cos(alpha2_rad) + self.z_heart2 * np.sin(alpha2_rad)
        y2_base = self.y_heart2
        z2_base = -self.x_heart2 * np.sin(alpha2_rad) + self.z_heart2 * np.cos(alpha2_rad)
        
        tempo_variation = abs(current_tempo - 75.0) / 75.0
        heartbeat2_scale = 1.0 + 0.15 * tempo_variation * (1.0 if current_tempo > 75 else 0.5)
        
        x2_rotated = x2_base * heartbeat2_scale
        y2_rotated = y2_base * heartbeat2_scale
        z2_rotated = z2_base * heartbeat2_scale
        x2_final = x2_rotated + 25  # Position: (25, 0, 0)
        y2_final = y2_rotated
        z2_final = z2_rotated
        
        # 3rd Heart (Loudness): Responds to RMS energy
        alpha3_deg = frame * 360 * tempo_factor / self.total_frames * 0.5  # Slower rotation
        alpha3_rad = np.deg2rad(alpha3_deg)
        
        x3_base = self.x_heart3 * np.cos(alpha3_rad) + self.z_heart3 * np.sin(alpha3_rad)
        y3_base = self.y_heart3
        z3_base = -self.x_heart3 * np.sin(alpha3_rad) + self.z_heart3 * np.cos(alpha3_rad)
        
        # Scale based on loudness
        heartbeat3_scale = 1.0 + 0.25 * loudness  # Louder = bigger
        
        x3_rotated = x3_base * heartbeat3_scale
        y3_rotated = y3_base * heartbeat3_scale
        z3_rotated = z3_base * heartbeat3_scale
        x3_final = x3_rotated  # Position: (0, 20, 0)
        y3_final = y3_rotated + 20
        z3_final = z3_rotated
        
        # 4th Heart (Bass): Responds to bass frequencies
        alpha4_deg = frame * 360 * tempo_factor / self.total_frames * 0.8  # Medium rotation
        alpha4_rad = np.deg2rad(alpha4_deg)
        
        x4_base = self.x_heart4 * np.cos(alpha4_rad) + self.z_heart4 * np.sin(alpha4_rad)
        y4_base = self.y_heart4
        z4_base = -self.x_heart4 * np.sin(alpha4_rad) + self.z_heart4 * np.cos(alpha4_rad)
        
        # Scale based on bass
        heartbeat4_scale = 1.0 + 0.2 * bass  # More bass = bigger
        
        x4_rotated = x4_base * heartbeat4_scale
        y4_rotated = y4_base * heartbeat4_scale
        z4_rotated = z4_base * heartbeat4_scale
        x4_final = x4_rotated  # Position: (0, 0, 25)
        y4_final = y4_rotated
        z4_final = z4_rotated + 25
        
        # 5th Heart (Onsets): Responds to onset detection
        alpha5_deg = frame * 360 * tempo_factor / self.total_frames * (-0.5)  # Counter-rotate slower
        alpha5_rad = np.deg2rad(alpha5_deg)
        
        x5_base = self.x_heart5 * np.cos(alpha5_rad) + self.z_heart5 * np.sin(alpha5_rad)
        y5_base = self.y_heart5
        z5_base = -self.x_heart5 * np.sin(alpha5_rad) + self.z_heart5 * np.cos(alpha5_rad)
        
        # Scale based on onsets
        heartbeat5_scale = 1.0 + 0.3 * onset_intensity  # Strong onsets = bigger pulse
        
        x5_rotated = x5_base * heartbeat5_scale
        y5_rotated = y5_base * heartbeat5_scale
        z5_rotated = z5_base * heartbeat5_scale
        x5_final = x5_rotated - 25  # Position: (-25, 0, 0)
        y5_final = y5_rotated
        z5_final = z5_rotated
        
        # Alpha values for all hearts
        alpha1 = 0.8 + 0.2 * bass
        alpha2 = 0.6 + 0.3 * bass
        alpha3 = 0.5 + 0.3 * loudness  # Loudness affects brightness
        alpha4 = 0.5 + 0.4 * bass  # Bass affects brightness most
        alpha5 = 0.5 + 0.3 * onset_intensity  # Onsets affect brightness
        alpha1 = min(1.0, max(0.0, alpha1))
        alpha2 = min(1.0, max(0.0, alpha2))
        alpha3 = min(1.0, max(0.0, alpha3))
        alpha4 = min(1.0, max(0.0, alpha4))
        alpha5 = min(1.0, max(0.0, alpha5))
        
        # Phase 1 (0-10%): Opening - Hearts appear sequentially
        if current_second < phase1_end:
            phase_t = current_second / phase1_end
            # Sequential appearance
            alpha1 = (0.8 + 0.2 * bass) * min(1.0, phase_t / 0.2)  # Appears first (0-20% of phase)
            alpha2 = (0.6 + 0.3 * bass) * max(0, min(1.0, (phase_t - 0.2) / 0.2))  # 20-40%
            alpha3 = (0.5 + 0.3 * loudness) * max(0, min(1.0, (phase_t - 0.4) / 0.2))  # 40-60%
            alpha4 = (0.5 + 0.4 * bass) * max(0, min(1.0, (phase_t - 0.6) / 0.2))  # 60-80%
            alpha5 = (0.5 + 0.3 * onset_intensity) * max(0, min(1.0, (phase_t - 0.8) / 0.2))  # 80-100%
            
            # Scale from small to normal
            scale1 = 0.1 + 0.9 * min(1.0, phase_t / 0.2)
            scale2 = 0.1 + 0.9 * max(0, min(1.0, (phase_t - 0.2) / 0.2))
            scale3 = 0.1 + 0.9 * max(0, min(1.0, (phase_t - 0.4) / 0.2))
            scale4 = 0.1 + 0.9 * max(0, min(1.0, (phase_t - 0.6) / 0.2))
            scale5 = 0.1 + 0.9 * max(0, min(1.0, (phase_t - 0.8) / 0.2))
            
            x1_final = x1_final * scale1
            y1_final = y1_final * scale1
            z1_final = z1_final * scale1
            x2_final = (x2_rotated + 25) * scale2
            y2_final = y2_rotated * scale2
            z2_final = z2_rotated * scale2
            x3_final = x3_rotated * scale3
            y3_final = (y3_rotated + 20) * scale3
            z3_final = z3_rotated * scale3
            x4_final = x4_rotated * scale4
            y4_final = y4_rotated * scale4
            z4_final = (z4_rotated + 25) * scale4
            x5_final = (x5_rotated - 25) * scale5
            y5_final = y5_rotated * scale5
            z5_final = z5_rotated * scale5
            
            # Camera: Wide frame to show all hearts
            base_zoom = 60 - 20 * phase_t  # 60 → 40
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 45 * phase_t
        
        # Phase 2 (10-25%): Establishment - All hearts establish their rhythms
        elif current_second < phase2_end:
            phase_t = (current_second - phase1_end) / (phase2_end - phase1_end)
            # Camera: Rotates to show all hearts
            base_zoom = 40 + 10 * np.sin(3 * np.pi * phase_t)  # 30-50 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 25 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 90 + 180 * phase_t
        
        # Phase 3 (25-40%): Development - Musical development
        elif current_second < phase3_end:
            phase_t = (current_second - phase2_end) / (phase3_end - phase2_end)
            # Camera: Orbital motion around center
            base_zoom = 35 + 10 * np.sin(4 * np.pi * phase_t)
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20 + 15 * np.sin(3 * np.pi * phase_t)
            azimuth = 270 + 360 * phase_t
        
        # Phase 4 (40-60%): Harmony - All hearts work in harmony
        elif current_second < phase4_end:
            phase_t = (current_second - phase3_end) / (phase4_end - phase3_end)
            # Camera: Dynamic switching between focus modes
            mode = int(phase_t * 5) % 5  # Cycle through 5 modes (one per heart)
            if mode == 0:
                # Focus on heart 1 (beats)
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            elif mode == 1:
                # Focus on heart 2 (tempo)
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            elif mode == 2:
                # Focus on heart 3 (loudness)
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 30
            elif mode == 3:
                # Focus on heart 4 (bass)
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            else:
                # Focus on heart 5 (onsets)
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            azimuth = 630 + 270 * phase_t
        
        # Phase 5 (60-75%): Climax - Maximum synchronization
        elif current_second < phase5_end:
            phase_t = (current_second - phase4_end) / (phase5_end - phase4_end)
            # All hearts at peak responsiveness
            base_zoom = 35 + 10 * np.sin(5 * np.pi * phase_t)  # 25-45 range
            zoom_factor = base_zoom - 4 * loudness
            elevation = 25 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 900 + 360 * phase_t
        
        # Phase 6 (75-90%): Peak synchronization
        elif current_second < phase6_end:
            phase_t = (current_second - phase5_end) / (phase6_end - phase5_end)
            # Rapid camera movements
            base_zoom = 30 + 15 * np.sin(6 * np.pi * phase_t)  # 15-45 range
            zoom_factor = base_zoom - 4 * loudness
            elevation = 20 + 20 * np.sin(5 * np.pi * phase_t)
            azimuth = 1260 + 540 * phase_t
        
        # Phase 7 (90-100%): Resolution - Gentle conclusion
        else:
            phase_t = (current_second - phase6_end) / (total_duration - phase6_end)
            # Hearts fade or maintain gentle motion
            fade_factor = 1.0 - 0.3 * phase_t
            alpha1 = (0.8 + 0.2 * bass) * fade_factor
            alpha2 = (0.6 + 0.3 * bass) * fade_factor
            alpha3 = (0.5 + 0.3 * loudness) * fade_factor
            alpha4 = (0.5 + 0.4 * bass) * fade_factor
            alpha5 = (0.5 + 0.3 * onset_intensity) * fade_factor
            alpha1 = min(1.0, max(0.0, alpha1))
            alpha2 = min(1.0, max(0.0, alpha2))
            alpha3 = min(1.0, max(0.0, alpha3))
            alpha4 = min(1.0, max(0.0, alpha4))
            alpha5 = min(1.0, max(0.0, alpha5))
            
            # Camera: Wide frame, gentle zoom out
            base_zoom = 40 + 60 * phase_t  # 40 → 100
            zoom_factor = base_zoom - 2 * loudness
            elevation = 25
            azimuth = 1800 + 90 * phase_t
        
        # Update all scatter plots
        self.scatter.set_alpha(alpha1)
        self.scatter._offsets3d = (x1_final, y1_final, z1_final)
        
        if self.scatter2 is not None:
            self.scatter2.set_alpha(alpha2)
            self.scatter2._offsets3d = (x2_final, y2_final, z2_final)
        
        if self.scatter3 is not None:
            self.scatter3.set_alpha(alpha3)
            self.scatter3._offsets3d = (x3_final, y3_final, z3_final)
        
        if self.scatter4 is not None:
            self.scatter4.set_alpha(alpha4)
            self.scatter4._offsets3d = (x4_final, y4_final, z4_final)
        
        if self.scatter5 is not None:
            self.scatter5.set_alpha(alpha5)
            self.scatter5._offsets3d = (x5_final, y5_final, z5_final)
        
        # Update camera
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Return all scatter plots
        result = [self.scatter]
        if self.scatter2 is not None:
            result.append(self.scatter2)
        if self.scatter3 is not None:
            result.append(self.scatter3)
        if self.scatter4 is not None:
            result.append(self.scatter4)
        if self.scatter5 is not None:
            result.append(self.scatter5)
        
        return tuple(result)


# Register the effect
register_effect('I2', EffectI2)


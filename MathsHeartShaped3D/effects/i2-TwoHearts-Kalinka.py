"""
Effect I2-TwoHearts-Kalinka: Two Hearts - Dual heart visualization with audio synchronization
1st heart syncs with beats, 2nd heart syncs with tempo
Customized for Kalinka music
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


class EffectI2TwoHeartsKalinka(BaseEffect):
    """Two Hearts: Dual heart visualization with beat and tempo synchronization for Kalinka."""
    
    def __init__(self, total_frames, fps, x_original, y_original, z_original, 
                 scatter, ax, audio_features=None, x_heart2=None, y_heart2=None, z_heart2=None, scatter2=None):
        """Initialize with second heart coordinates and scatter plot."""
        super().__init__(total_frames, fps, x_original, y_original, z_original, 
                        scatter, ax, audio_features)
        self.x_heart2 = x_heart2 if x_heart2 is not None else x_original
        self.y_heart2 = y_heart2 if y_heart2 is not None else y_original
        self.z_heart2 = z_heart2 if z_heart2 is not None else z_original
        self.scatter2 = scatter2  # Second scatter plot for 2nd heart
    
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
        phase1_end = total_duration * 0.08   # 0-8%: Opening
        phase2_end = total_duration * 0.20   # 8-20%: Establishment
        phase3_end = total_duration * 0.25   # 20-25%: First Through-Heart
        phase4_end = total_duration * 0.45   # 25-45%: Development
        phase5_end = total_duration * 0.50  # 45-50%: Second Through-Heart
        phase6_end = total_duration * 0.70  # 50-70%: Harmony
        phase7_end = total_duration * 0.75   # 70-75%: Third Through-Heart
        phase8_end = total_duration * 0.90   # 75-90%: Climax
        phase9_end = total_duration * 0.93   # 90-93%: Fourth Through-Heart
        # phase10: 93-100% - Resolution
        
        # 1st Heart: Rotates based on tempo, pulses on beats
        tempo_factor = current_tempo / 60.0  # Normalize to 60 BPM baseline
        alpha1_deg = frame * 360 * tempo_factor / self.total_frames
        alpha1_rad = np.deg2rad(alpha1_deg)
        
        x1_base = self.x_original * np.cos(alpha1_rad) + self.z_original * np.sin(alpha1_rad)
        y1_base = self.y_original
        z1_base = -self.x_original * np.sin(alpha1_rad) + self.z_original * np.cos(alpha1_rad)
        
        # 1st heart heartbeat pulse synchronized with beats
        heartbeat1_scale = 1.0
        if beat_intensity > 0:
            heartbeat1_scale = 1.0 + 0.2 * beat_intensity  # Stronger pulse on beats
        if onset_intensity > 0.5:
            heartbeat1_scale = max(heartbeat1_scale, 1.0 + 0.15 * onset_intensity)
        
        x1_rotated = x1_base * heartbeat1_scale
        y1_rotated = y1_base * heartbeat1_scale
        z1_rotated = z1_base * heartbeat1_scale
        
        # 1st heart position: (0, 0, 0) - center origin
        x1_final = x1_rotated
        y1_final = y1_rotated
        z1_final = z1_rotated
        
        # 2nd Heart: Independent rotation, syncs with tempo
        # Counter-rotating for visual interest
        alpha2_deg = frame * 360 * tempo_factor / self.total_frames * (-0.7)  # Counter-rotate at 70% speed
        alpha2_rad = np.deg2rad(alpha2_deg)
        
        x2_base = self.x_heart2 * np.cos(alpha2_rad) + self.z_heart2 * np.sin(alpha2_rad)
        y2_base = self.y_heart2
        z2_base = -self.x_heart2 * np.sin(alpha2_rad) + self.z_heart2 * np.cos(alpha2_rad)
        
        # 2nd heart pulse: gentler, responds to tempo changes
        # Use tempo variation for pulse
        tempo_variation = abs(current_tempo - 75.0) / 75.0  # Normalized tempo change
        heartbeat2_scale = 1.0 + 0.15 * tempo_variation * (1.0 if current_tempo > 75 else 0.5)
        
        x2_rotated = x2_base * heartbeat2_scale
        y2_rotated = y2_base * heartbeat2_scale
        z2_rotated = z2_base * heartbeat2_scale
        
        # 2nd heart position: (25, 0, 0) - offset 25 units along X-axis
        x2_final = x2_rotated + 25
        y2_final = y2_rotated
        z2_final = z2_rotated
        
        # Alpha values for both hearts
        alpha1 = 0.8 + 0.2 * bass  # 1st heart: 0.8-1.0 based on bass
        alpha2 = 0.6 + 0.3 * bass  # 2nd heart: 0.6-0.9 (more transparent)
        alpha1 = min(1.0, max(0.0, alpha1))
        alpha2 = min(1.0, max(0.0, alpha2))
        
        # Phase 1 (0-8%): Opening - Both hearts fade in from darkness
        if current_second < phase1_end:
            phase_t = current_second / phase1_end
            # 1st heart appears first
            alpha1 = (0.8 + 0.2 * bass) * phase_t
            alpha1 = min(1.0, max(0.0, alpha1))
            # 2nd heart appears shortly after
            alpha2 = (0.6 + 0.3 * bass) * max(0, (phase_t - 0.3) / 0.7)  # Starts at 30% of phase
            alpha2 = min(1.0, max(0.0, alpha2))
            
            # Scale both hearts from small to normal
            scale1 = 0.1 + 0.9 * phase_t
            scale2 = 0.1 + 0.9 * max(0, (phase_t - 0.3) / 0.7)
            x1_final = x1_final * scale1
            y1_final = y1_final * scale1
            z1_final = z1_final * scale1
            x2_final = x2_final * scale2
            y2_final = y2_final * scale2
            z2_final = z2_final * scale2
            
            # Camera: Wide frame showing both hearts
            base_zoom = 50 - 15 * phase_t  # 50 → 35 (wider for dual view)
            zoom_factor = base_zoom - 3 * loudness
            elevation = 25 + 5 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 45 * phase_t
        
        # Phase 2 (8-20%): Establishment - Hearts establish their rhythms
        elif current_second < phase2_end:
            phase_t = (current_second - phase1_end) / (phase2_end - phase1_end)
            # Camera: Alternates between dual-frame and individual focus
            if phase_t < 0.5:
                # Dual-frame mode
                base_zoom = 35 + 5 * np.sin(4 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 25 + 5 * np.sin(2 * np.pi * phase_t)
                azimuth = 90 + 90 * phase_t
            else:
                # Focus on 1st heart
                base_zoom = 20 + 5 * np.sin(4 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20 + 5 * np.sin(2 * np.pi * phase_t)
                azimuth = 90 + 90 * phase_t
        
        # Phase 3 (20-25%): First Through-Heart Passage - Pass through 1st heart
        elif current_second < phase3_end:
            phase_t = (current_second - phase2_end) / (phase3_end - phase2_end)
            alpha1 = 0.9 + 0.1 * bass
            alpha1 = min(1.0, max(0.0, alpha1))
            # Through-heart: 30 → -15 → 25
            if phase_t < 0.6:
                # Going through
                zoom_factor = 30 - 45 * ((phase_t / 0.6) ** 1.5)
            else:
                # Exiting
                zoom_factor = -15 + 40 * ((phase_t - 0.6) / 0.4)
            elevation = 20 + 15 * np.sin(np.pi * phase_t)
            azimuth = 180 + 90 * phase_t
        
        # Phase 4 (25-45%): Development - Musical development
        elif current_second < phase4_end:
            phase_t = (current_second - phase3_end) / (phase4_end - phase3_end)
            # Camera: Orbital motion around both hearts
            base_zoom = 30 + 10 * np.sin(3 * np.pi * phase_t)  # 20-40 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 270 + 360 * phase_t  # Full orbit
        
        # Phase 5 (45-50%): Second Through-Heart Passage - Pass through 2nd heart
        elif current_second < phase5_end:
            phase_t = (current_second - phase4_end) / (phase5_end - phase4_end)
            alpha2 = 0.9 + 0.1 * bass
            alpha2 = min(1.0, max(0.0, alpha2))
            # Through-heart: 35 → -20 → 30
            if phase_t < 0.6:
                zoom_factor = 35 - 55 * ((phase_t / 0.6) ** 2)
            else:
                zoom_factor = -20 + 50 * ((phase_t - 0.6) / 0.4)
            elevation = 18 + 20 * np.sin(np.pi * phase_t)
            azimuth = 630 + 120 * phase_t
        
        # Phase 6 (50-70%): Harmony - Hearts work in harmony
        elif current_second < phase6_end:
            phase_t = (current_second - phase5_end) / (phase6_end - phase5_end)
            # Both hearts pulse together on strong beats (already applied in base calculation)
            # Additional pulse on very strong beats
            if beat_intensity > 0.7:
                extra_scale1 = 1.0 + 0.1 * (beat_intensity - 0.7) / 0.3
                extra_scale2 = 1.0 + 0.08 * (beat_intensity - 0.7) / 0.3
                x1_final = x1_rotated * extra_scale1
                y1_final = y1_rotated * extra_scale1
                z1_final = z1_rotated * extra_scale1
                x2_final = x2_rotated * extra_scale2 + 25
                y2_final = y2_rotated * extra_scale2
                z2_final = z2_rotated * extra_scale2
            
            # Camera: Dynamic switching between focus modes
            mode = int(phase_t * 4) % 3  # Cycle through 3 modes
            if mode == 0:
                # Dual-frame
                base_zoom = 40 + 5 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 25
            elif mode == 1:
                # Focus on 1st heart
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            else:
                # Focus on 2nd heart
                base_zoom = 20 + 3 * np.sin(2 * np.pi * phase_t)
                zoom_factor = base_zoom - 3 * loudness
                elevation = 20
            azimuth = 750 + 270 * phase_t
        
        # Phase 7 (70-75%): Third Through-Heart Passage - Peak musical moment
        elif current_second < phase7_end:
            phase_t = (current_second - phase6_end) / (phase7_end - phase6_end)
            alpha1 = 1.0  # Maximum brightness
            alpha2 = 1.0
            # Through-heart: 30 → -15 → 25
            if phase_t < 0.6:
                zoom_factor = 30 - 45 * ((phase_t / 0.6) ** 1.8)
            else:
                zoom_factor = -15 + 40 * ((phase_t - 0.6) / 0.4)
            elevation = 15 + 25 * np.sin(np.pi * phase_t)
            azimuth = 1020 + 180 * phase_t
        
        # Phase 8 (75-90%): Climax - Maximum synchronization
        elif current_second < phase8_end:
            phase_t = (current_second - phase7_end) / (phase8_end - phase7_end)
            # Both hearts at peak responsiveness
            alpha1 = 0.8 + 0.2 * bass
            alpha2 = 0.6 + 0.4 * bass  # 2nd heart can get brighter too
            alpha1 = min(1.0, max(0.0, alpha1))
            alpha2 = min(1.0, max(0.0, alpha2))
            
            # Camera: Rapid switching, dynamic movements
            base_zoom = 18 + 7 * np.sin(5 * np.pi * phase_t)  # 11-25 range
            zoom_factor = base_zoom - 4 * loudness
            elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 1200 + 360 * phase_t
        
        # Phase 9 (90-93%): Fourth Through-Heart Passage - Final dramatic passage
        elif current_second < phase9_end:
            phase_t = (current_second - phase8_end) / (phase9_end - phase8_end)
            # Pass between both hearts
            if phase_t < 0.5:
                zoom_factor = 35 - 50 * ((phase_t / 0.5) ** 1.5)
            else:
                zoom_factor = -15 + 45 * ((phase_t - 0.5) / 0.5)
            elevation = 20 + 18 * np.sin(np.pi * phase_t)
            azimuth = 1560 + 90 * phase_t
        
        # Phase 10 (93-100%): Resolution - Gentle conclusion
        else:
            phase_t = (current_second - phase9_end) / (total_duration - phase9_end)
            # Hearts fade or maintain gentle motion
            alpha1 = (0.8 + 0.2 * bass) * (1.0 - 0.3 * phase_t)
            alpha2 = (0.6 + 0.3 * bass) * (1.0 - 0.3 * phase_t)
            alpha1 = min(1.0, max(0.0, alpha1))
            alpha2 = min(1.0, max(0.0, alpha2))
            
            # Camera: Wide frame, gentle zoom out
            base_zoom = 30 + 70 * phase_t  # 30 → 100
            zoom_factor = base_zoom - 2 * loudness
            elevation = 20
            azimuth = 1650 + 90 * phase_t
        
        # Update scatter plots
        self.scatter.set_alpha(alpha1)
        self.scatter._offsets3d = (x1_final, y1_final, z1_final)
        
        if self.scatter2 is not None:
            self.scatter2.set_alpha(alpha2)
            self.scatter2._offsets3d = (x2_final, y2_final, z2_final)
        
        # Update camera
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        # Return both scatter plots
        if self.scatter2 is not None:
            return self.scatter, self.scatter2
        else:
            return self.scatter,


# Register the effect
register_effect('I2-TwoHearts-Kalinka', EffectI2TwoHeartsKalinka)


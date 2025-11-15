"""
Effect H8sync3min: Heart Genesis with Real Audio Sync - Extended 3.5 minute version
Based on H8sync but extended to 210 seconds (3:30) with additional artistic phases
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


class EffectH8sync3min(BaseEffect):
    """Heart Genesis with Real Audio Sync - Extended 3.5 minute version."""
    
    def get_total_frames(self):
        return 6300  # 210 seconds (3:30) at 30 fps
    
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
        
        # Heart rotates slowly (360 degrees total for longer animation, tempo-adjusted)
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
        
        # Phase 1-8: Same as H8sync (0-100s)
        if current_second < 10.0:
            # Phase 1: Empty black space, then gradually heart appears
            phase_t = current_second / 10.0
            point_alpha = 0.8 * phase_t
            scale = 0.1 + 0.9 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
            base_zoom = 200 - 175 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20
            azimuth = 45
        
        elif current_second < 25.0:
            # Phase 2: Energy burst, strings ascending
            phase_t = (current_second - 10.0) / 15.0
            point_alpha = 0.8
            base_zoom = 25 - 5 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20
            azimuth = 45 + 90 * phase_t
        
        elif current_second < 40.0:
            # Phase 3: Strings coalesce
            phase_t = (current_second - 25.0) / 15.0
            point_alpha = 0.8
            base_zoom = 20 - 3 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20 + 10 * np.sin(np.pi * phase_t)
            azimuth = 135 + 90 * phase_t
        
        elif current_second < 60.0:
            # Phase 4: Heartbeat rhythm
            phase_t = (current_second - 40.0) / 20.0
            point_alpha = 0.8
            zoom_factor = 17 - 5 * loudness
            elevation = 20
            azimuth = 225 + 180 * phase_t
        
        elif current_second < 75.0:
            # Phase 5: Majestic orchestral
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 0.8
            base_zoom = 17 + 3 * np.sin(2 * np.pi * phase_t)
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 405 + 360 * phase_t
        
        elif current_second < 90.0:
            # Phase 6: Cosmic expansion
            phase_t = (current_second - 75.0) / 15.0
            point_alpha = 0.6 + 0.4 * bass + 0.2 * phase_t
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 20 + 80 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 40 - 20 * phase_t
            azimuth = 585 + 90 * phase_t
        
        elif current_second < 95.0:
            # Phase 7: Mathematical precision
            phase_t = (current_second - 90.0) / 5.0
            point_alpha = 0.6 + 0.4 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            zoom_factor = 100 - 5 * loudness
            elevation = 20
            azimuth = 675
        
        elif current_second < 100.0:
            # Phase 8: Fade to silence, infinite stars
            phase_t = (current_second - 95.0) / 5.0
            point_alpha = (0.6 + 0.4 * bass) * (1.0 - phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            base_zoom = 100 + 100 * phase_t
            zoom_factor = base_zoom - 5 * loudness
            elevation = 20
            azimuth = 675
        
        # Phase 9 (100-130s): Spiral Descent - Camera spirals down while heart pulses with bass
        elif current_second < 130.0:
            phase_t = (current_second - 100.0) / 30.0
            # Brightness syncs with bass
            point_alpha = 0.5 + 0.5 * bass + 0.1 * np.sin(4 * np.pi * phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            # Spiral descent: elevation decreases while azimuth rotates
            elevation = 60 - 40 * phase_t  # From 60 to 20 degrees
            azimuth = 675 + 720 * phase_t  # 2 full rotations
            # Zoom pulses with bass
            base_zoom = 150 - 50 * phase_t  # Zoom in from 150 to 100
            zoom_factor = base_zoom - 10 * bass - 5 * loudness
            # Heart pulses more dramatically on beats
            if beat_intensity > 0:
                pulse = 1.0 + 0.3 * beat_intensity
                x_rotated = x_rotated * pulse
                y_rotated = y_rotated * pulse
                z_rotated = z_rotated * pulse
        
        # Phase 10 (130-160s): Kaleidoscope Transformation - Heart multiplies and mirrors
        elif current_second < 160.0:
            phase_t = (current_second - 130.0) / 30.0
            point_alpha = 0.7 + 0.3 * bass
            point_alpha = min(1.0, max(0.0, point_alpha))
            
            # Create kaleidoscope effect by rotating and mirroring
            # Multiple rotation angles for kaleidoscope
            num_mirrors = int(4 + 4 * phase_t)  # 4 to 8 mirrors
            angles = np.linspace(0, 2 * np.pi, num_mirrors, endpoint=False)
            
            # Use first mirror for main heart (simplified - full implementation would need multiple hearts)
            mirror_angle = angles[0] + phase_t * 2 * np.pi
            cos_a = np.cos(mirror_angle)
            sin_a = np.sin(mirror_angle)
            x_mirror = x_rotated * cos_a - z_rotated * sin_a
            z_mirror = x_rotated * sin_a + z_rotated * cos_a
            x_rotated = x_mirror
            z_rotated = z_mirror
            
            # Camera orbits rapidly
            elevation = 20 + 30 * np.sin(3 * np.pi * phase_t)
            azimuth = 1395 + 1080 * phase_t  # 3 full rotations
            zoom_factor = 100 - 30 * phase_t - 10 * bass  # Continue zooming in
            # Pulse on onsets
            if onset_intensity > 0.3:
                pulse = 1.0 + 0.25 * onset_intensity
                x_rotated = x_rotated * pulse
                y_rotated = y_rotated * pulse
                z_rotated = z_rotated * pulse
        
        # Phase 11 (160-180s): Cosmic Dance - Heart orbits in complex patterns
        elif current_second < 180.0:
            phase_t = (current_second - 160.0) / 20.0
            # Brightness follows loudness
            point_alpha = 0.6 + 0.4 * loudness
            point_alpha = min(1.0, max(0.0, point_alpha))
            
            # Complex orbital motion: figure-8 combined with spiral
            orbit_radius = 5 * np.sin(2 * np.pi * phase_t)
            orbit_angle = 4 * np.pi * phase_t
            x_rotated = x_rotated + orbit_radius * np.cos(orbit_angle)
            z_rotated = z_rotated + orbit_radius * np.sin(orbit_angle)
            
            # Camera follows complex path
            elevation = 30 + 25 * np.sin(4 * np.pi * phase_t) + 10 * np.cos(6 * np.pi * phase_t)
            azimuth = 2475 + 540 * phase_t  # 1.5 rotations
            zoom_factor = 70 - 20 * phase_t - 8 * loudness  # Continue zooming
            # Strong pulse on beats
            if beat_intensity > 0:
                pulse = 1.0 + 0.35 * beat_intensity
                x_rotated = x_rotated * pulse
                y_rotated = y_rotated * pulse
                z_rotated = z_rotated * pulse
        
        # Phase 12 (180-200s): Energy Convergence - Dramatic zoom in with bass sync
        elif current_second < 200.0:
            phase_t = (current_second - 180.0) / 20.0
            # Brightness peaks with bass
            point_alpha = 0.5 + 0.5 * bass + 0.2 * np.sin(8 * np.pi * phase_t)
            point_alpha = min(1.0, max(0.0, point_alpha))
            
            # Dramatic zoom in (accelerating)
            base_zoom = 50 - 40 * (phase_t ** 2)  # Accelerating zoom: 50 to 10
            zoom_factor = base_zoom - 15 * bass - 10 * loudness
            
            # Camera elevation sweeps dramatically
            elevation = 50 - 40 * phase_t + 20 * np.sin(4 * np.pi * phase_t)
            azimuth = 3015 + 360 * phase_t  # 1 rotation
            
            # Heart pulses intensely on beats and bass
            pulse = 1.0
            if beat_intensity > 0:
                pulse = max(pulse, 1.0 + 0.4 * beat_intensity)
            if bass > 0.7:
                pulse = max(pulse, 1.0 + 0.3 * bass)
            x_rotated = x_rotated * pulse
            y_rotated = y_rotated * pulse
            z_rotated = z_rotated * pulse
        
        # Phase 13 (200-210s): Final Crescendo - Explosive expansion then fade
        else:
            phase_t = (current_second - 200.0) / 10.0
            # Brightness peaks then fades
            if phase_t < 0.5:
                # Peak brightness
                point_alpha = 0.7 + 0.3 * bass + 0.2 * (1.0 - 2 * phase_t)
            else:
                # Fade out
                point_alpha = (0.7 + 0.3 * bass) * (1.0 - (phase_t - 0.5) * 2)
            point_alpha = min(1.0, max(0.0, point_alpha))
            
            # Explosive zoom out
            if phase_t < 0.5:
                zoom_factor = 10 + 90 * (phase_t * 2) ** 2  # Rapid expansion: 10 to 100
            else:
                zoom_factor = 100 + 200 * ((phase_t - 0.5) * 2) ** 2  # Continue to 300
            
            elevation = 10 + 10 * np.sin(8 * np.pi * phase_t)
            azimuth = 3375 + 180 * phase_t  # Half rotation
            
            # Final pulse on strong beats
            if beat_intensity > 0.5:
                pulse = 1.0 + 0.5 * beat_intensity
                x_rotated = x_rotated * pulse
                y_rotated = y_rotated * pulse
                z_rotated = z_rotated * pulse
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H8sync3min', EffectH8sync3min)


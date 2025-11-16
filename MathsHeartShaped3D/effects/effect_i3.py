"""
Effect I3: Birthday Celebration - 11, 16, 2025
Variable number of hearts (11 hearts, then 16 hearts) with number display
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


class EffectI3(BaseEffect):
    """Birthday Celebration: 11 hearts, then 16 hearts, with number display (11, 16, 2025)."""
    
    def __init__(self, total_frames, fps, x_original, y_original, z_original, 
                 scatter, ax, audio_features=None, heart_data_list=None, text_display=None):
        """
        Initialize with list of heart data.
        
        heart_data_list: List of tuples (x, y, z, scatter, colormap_name) for each heart
        text_display: Function or object to handle text display
        """
        super().__init__(total_frames, fps, x_original, y_original, z_original, 
                        scatter, ax, audio_features)
        self.heart_data_list = heart_data_list if heart_data_list is not None else []
        self.text_display = text_display
        self.number_texts = {}  # Store text objects for numbers
        self._init_number_texts()
    
    def _init_number_texts(self):
        """Initialize text objects for number display."""
        # Create text objects for numbers (will be shown/hidden as needed)
        # Using 2D text overlay on the figure
        self.number_texts['11'] = None
        self.number_texts['16'] = None
        self.number_texts['2025'] = None
    
    def get_total_frames(self):
        # Calculate duration from audio features if available, otherwise use default
        if self.audio_features and 'rms_times' in self.audio_features:
            rms_times = self.audio_features.get('rms_times', [])
            if len(rms_times) > 0:
                duration = rms_times[-1]  # Last RMS timestamp approximates duration
                return int(duration * self.fps)
        
        # Fallback: 60 seconds at 30 fps
        return 1800  # 60 seconds * 30 fps
    
    def _get_heart_positions_11(self):
        """Generate positions for 11 hearts in a formation."""
        positions = []
        # Arrange in a pattern: center + 10 around it
        # Pattern: 1 center, 5 in inner circle, 5 in outer positions
        center = (0, 0, 0)
        positions.append(center)
        
        # Inner circle: 5 hearts
        inner_radius = 20
        for i in range(5):
            angle = 2 * np.pi * i / 5
            x = inner_radius * np.cos(angle)
            z = inner_radius * np.sin(angle)
            positions.append((x, 0, z))
        
        # Outer positions: 5 hearts
        outer_radius = 35
        for i in range(5):
            angle = 2 * np.pi * i / 5 + np.pi / 5  # Offset by half step
            x = outer_radius * np.cos(angle)
            z = outer_radius * np.sin(angle)
            positions.append((x, 0, z))
        
        return positions
    
    def _get_heart_positions_16(self):
        """Generate positions for 16 hearts in a formation."""
        positions = []
        # Arrange in a 4x4 grid pattern (with some 3D variation)
        grid_size = 4
        spacing = 18
        start_offset = -spacing * 1.5
        
        for i in range(grid_size):
            for j in range(grid_size):
                x = start_offset + j * spacing
                z = start_offset + i * spacing
                y = 2 * np.sin(i * np.pi / 3) * np.cos(j * np.pi / 3)  # Slight 3D variation
                positions.append((x, y, z))
        
        return positions
    
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
        phase1_end = total_duration * 0.10   # 0-10%: Opening
        phase2_end = total_duration * 0.20   # 10-20%: 11 Hearts Formation
        phase3_end = total_duration * 0.35   # 20-35%: 11 Hearts Synchronization
        phase4_end = total_duration * 0.45   # 35-45%: Transition Preparation
        phase5_end = total_duration * 0.55   # 45-55%: Transition to 16 Hearts
        phase6_end = total_duration * 0.75   # 55-75%: 16 Hearts Synchronization
        phase7_end = total_duration * 0.90   # 75-90%: Celebration Peak
        # phase8: 90-100% - Finale
        
        # Determine number of hearts to display
        if current_second < phase5_end:
            # Phase 1-4: 11 hearts
            num_hearts = 11
            heart_positions = self._get_heart_positions_11()
        else:
            # Phase 5-8: 16 hearts
            num_hearts = 16
            heart_positions = self._get_heart_positions_16()
        
        # Limit to available hearts
        num_hearts = min(num_hearts, len(self.heart_data_list))
        
        # Colormaps for hearts (cycle through different colormaps)
        colormaps = ['magma', 'YlOrRd', 'Blues', 'Greens', 'Purples', 'plasma', 'viridis', 
                     'cool', 'hot', 'spring', 'summer', 'autumn', 'winter', 'coolwarm', 
                     'RdYlBu', 'Spectral']
        
        # Process each heart
        tempo_factor = current_tempo / 60.0
        result_scatters = []
        
        for i in range(num_hearts):
            if i >= len(self.heart_data_list):
                break
            
            x_orig, y_orig, z_orig, scatter_obj, colormap_name = self.heart_data_list[i]
            
            # Rotation speed varies by heart (50%-100% of tempo)
            rotation_speed = 0.5 + 0.5 * (i % 5) / 4.0  # Varies from 0.5 to 1.0
            if i % 2 == 1:
                rotation_speed = -rotation_speed  # Counter-rotate some hearts
            
            alpha_deg = frame * 360 * tempo_factor * rotation_speed / self.total_frames
            alpha_rad = np.deg2rad(alpha_deg)
            
            # Rotate heart
            x_base = x_orig * np.cos(alpha_rad) + z_orig * np.sin(alpha_rad)
            y_base = y_orig
            z_base = -x_orig * np.sin(alpha_rad) + z_orig * np.cos(alpha_rad)
            
            # Assign audio feature to heart (distribute features across hearts)
            feature_type = i % 5  # Cycle through 5 features
            heartbeat_scale = 1.0
            
            if feature_type == 0:  # Beats
                if beat_intensity > 0:
                    heartbeat_scale = 1.0 + 0.2 * beat_intensity
            elif feature_type == 1:  # Tempo
                tempo_variation = abs(current_tempo - 75.0) / 75.0
                heartbeat_scale = 1.0 + 0.15 * tempo_variation
            elif feature_type == 2:  # Loudness
                heartbeat_scale = 1.0 + 0.25 * loudness
            elif feature_type == 3:  # Bass
                heartbeat_scale = 1.0 + 0.2 * bass
            else:  # Onsets
                heartbeat_scale = 1.0 + 0.3 * onset_intensity
            
            x_rotated = x_base * heartbeat_scale
            y_rotated = y_base * heartbeat_scale
            z_rotated = z_base * heartbeat_scale
            
            # Apply position offset
            pos_x, pos_y, pos_z = heart_positions[i] if i < len(heart_positions) else (0, 0, 0)
            x_final = x_rotated + pos_x
            y_final = y_rotated + pos_y
            z_final = z_rotated + pos_z
            
            # Alpha based on feature
            if feature_type == 0:
                alpha = 0.5 + 0.4 * (0.5 + 0.5 * beat_intensity)
            elif feature_type == 1:
                alpha = 0.5 + 0.4 * (0.5 + 0.5 * (current_tempo / 150.0))
            elif feature_type == 2:
                alpha = 0.5 + 0.3 * loudness
            elif feature_type == 3:
                alpha = 0.5 + 0.4 * bass
            else:
                alpha = 0.5 + 0.3 * onset_intensity
            
            alpha = min(1.0, max(0.0, alpha))
            
            # Phase-specific adjustments
            if current_second < phase1_end:
                # Opening: Sequential appearance
                phase_t = current_second / phase1_end
                appear_t = i / num_hearts  # Each heart appears at different time
                if phase_t < appear_t + 0.1:
                    alpha = alpha * max(0, (phase_t - appear_t) / 0.1)
                scale = 0.1 + 0.9 * max(0, min(1.0, (phase_t - appear_t) / 0.1))
                x_final = x_final * scale
                y_final = y_final * scale
                z_final = z_final * scale
            
            elif current_second < phase5_end and num_hearts == 11:
                # 11 hearts phase: Normal operation
                pass
            elif current_second >= phase4_end and current_second < phase5_end:
                # Transition: Fade out 11 hearts, prepare for 16
                phase_t = (current_second - phase4_end) / (phase5_end - phase4_end)
                alpha = alpha * (1.0 - phase_t * 0.5)  # Fade out partially
            elif current_second >= phase5_end and num_hearts == 16:
                # 16 hearts phase: Normal operation
                if current_second < phase5_end + (phase6_end - phase5_end) * 0.2:
                    # Transition in: Fade in new hearts
                    phase_t = (current_second - phase5_end) / ((phase6_end - phase5_end) * 0.2)
                    if i >= 11:  # New hearts (11-15)
                        alpha = alpha * min(1.0, phase_t)
                    else:  # Existing hearts
                        alpha = alpha * (0.5 + 0.5 * min(1.0, phase_t))
            
            # Update scatter plot
            scatter_obj.set_alpha(alpha)
            scatter_obj._offsets3d = (x_final, y_final, z_final)
            result_scatters.append(scatter_obj)
        
        # Number display
        self._update_number_display(current_second, total_duration, phase2_end, phase5_end, phase7_end)
        
        # Camera settings
        if current_second < phase1_end:
            phase_t = current_second / phase1_end
            base_zoom = 60 - 10 * phase_t  # 60 → 50
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 45 * phase_t
        elif current_second < phase2_end:
            phase_t = (current_second - phase1_end) / (phase2_end - phase1_end)
            base_zoom = 50 + 20 * np.sin(3 * np.pi * phase_t)  # 50-70 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 90 + 90 * phase_t
        elif current_second < phase3_end:
            phase_t = (current_second - phase2_end) / (phase3_end - phase2_end)
            base_zoom = 60 + 10 * np.sin(4 * np.pi * phase_t)  # 50-70 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 10 * np.sin(3 * np.pi * phase_t)
            azimuth = 180 + 180 * phase_t
        elif current_second < phase4_end:
            phase_t = (current_second - phase3_end) / (phase4_end - phase3_end)
            base_zoom = 60 + 10 * np.sin(2 * np.pi * phase_t)
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30
            azimuth = 360 + 90 * phase_t
        elif current_second < phase5_end:
            phase_t = (current_second - phase4_end) / (phase5_end - phase4_end)
            base_zoom = 70 + 10 * phase_t  # 70 → 80 (wider for 16 hearts)
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 5 * np.sin(2 * np.pi * phase_t)
            azimuth = 450 + 90 * phase_t
        elif current_second < phase6_end:
            phase_t = (current_second - phase5_end) / (phase6_end - phase5_end)
            base_zoom = 70 + 10 * np.sin(3 * np.pi * phase_t)  # 60-80 range
            zoom_factor = base_zoom - 3 * loudness
            elevation = 30 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 540 + 360 * phase_t
        elif current_second < phase7_end:
            phase_t = (current_second - phase6_end) / (phase7_end - phase6_end)
            base_zoom = 65 + 15 * np.sin(5 * np.pi * phase_t)  # 50-80 range
            zoom_factor = base_zoom - 4 * loudness
            elevation = 30 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 900 + 540 * phase_t
        else:
            phase_t = (current_second - phase7_end) / (total_duration - phase7_end)
            base_zoom = 70 + 30 * phase_t  # 70 → 100
            zoom_factor = base_zoom - 2 * loudness
            elevation = 30
            azimuth = 1440 + 90 * phase_t
        
        # Update camera
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return tuple(result_scatters)
    
    def _update_number_display(self, current_second, total_duration, phase2_end, phase5_end, phase7_end):
        """Update number display (11, 16, 2025) using text overlay."""
        # Clear previous texts
        for text_obj in self.number_texts.values():
            if text_obj is not None:
                try:
                    text_obj.remove()
                except:
                    pass
        
        # Determine which number to show
        show_11 = False
        show_16 = False
        show_2025 = False
        
        # Show "11" during 11-heart phase
        if current_second < phase5_end:
            # Show at 11% of total duration or during 11-heart phase
            if current_second >= total_duration * 0.11 and current_second < phase5_end * 0.8:
                show_11 = True
        
        # Show "16" during 16-heart phase
        if current_second >= phase5_end:
            # Show at 16% into the 16-heart phase or during phase
            phase_16_start = phase5_end
            phase_16_duration = total_duration - phase_16_start
            phase_16_t = (current_second - phase_16_start) / phase_16_duration if phase_16_duration > 0 else 0
            if phase_16_t >= 0.16 and phase_16_t < 0.85:
                show_16 = True
        
        # Show "2025" at the end
        if current_second >= phase7_end:
            show_2025 = True
        
        # Create text objects (using figure text, not 3D text for simplicity)
        fig = self.ax.figure
        
        if show_11:
            if self.number_texts['11'] is None or not hasattr(self.number_texts['11'], 'get_figure'):
                self.number_texts['11'] = fig.text(0.5, 0.85, '11', 
                                                   fontsize=72, ha='center', va='center',
                                                   color='white', alpha=0.7, weight='bold')
            else:
                self.number_texts['11'].set_alpha(0.7)
        else:
            if self.number_texts['11'] is not None:
                self.number_texts['11'].set_alpha(0.0)
        
        if show_16:
            if self.number_texts['16'] is None or not hasattr(self.number_texts['16'], 'get_figure'):
                self.number_texts['16'] = fig.text(0.5, 0.85, '16', 
                                                   fontsize=72, ha='center', va='center',
                                                   color='white', alpha=0.7, weight='bold')
            else:
                self.number_texts['16'].set_alpha(0.7)
        else:
            if self.number_texts['16'] is not None:
                self.number_texts['16'].set_alpha(0.0)
        
        if show_2025:
            if self.number_texts['2025'] is None or not hasattr(self.number_texts['2025'], 'get_figure'):
                self.number_texts['2025'] = fig.text(0.5, 0.5, '2025', 
                                                      fontsize=96, ha='center', va='center',
                                                      color='white', alpha=0.8, weight='bold')
            else:
                self.number_texts['2025'].set_alpha(0.8)
        else:
            if self.number_texts['2025'] is not None:
                self.number_texts['2025'].set_alpha(0.0)


# Register the effect
register_effect('I3', EffectI3)


"""
Effect H8: Heart Genesis with Music Sync (BPM-synchronized beats - 100 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH8(BaseEffect):
    """Heart Genesis with Music Sync: BPM-synchronized beats."""
    
    def get_total_frames(self):
        return 3000  # 100 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Heart rotates slowly (180 degrees total)
        alpha_deg = frame * 180 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_base = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_base = self.y_original
        z_base = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Base scale (no heartbeat yet)
        heartbeat_scale = 1.0
        
        # Calculate heartbeat pulses at BPM transition points
        # Each heartbeat is a quick pulse (0.3 seconds) at the transition
        heartbeat_duration = 0.3  # 0.3 seconds for each heartbeat
        
        # BPM transition points where heartbeats occur
        if abs(current_second - 10.0) < heartbeat_duration:  # 60→75 BPM at 0:10
            beat_t = abs(current_second - 10.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)  # Quick pulse
        elif abs(current_second - 25.0) < heartbeat_duration:  # 75→80 BPM at 0:25
            beat_t = abs(current_second - 25.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        elif abs(current_second - 40.0) < heartbeat_duration:  # 80→85 BPM at 0:40
            beat_t = abs(current_second - 40.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        elif abs(current_second - 60.0) < heartbeat_duration:  # 85→90 BPM at 1:00
            beat_t = abs(current_second - 60.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        elif abs(current_second - 75.0) < heartbeat_duration:  # 90→75 BPM at 1:15
            beat_t = abs(current_second - 75.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        elif abs(current_second - 90.0) < heartbeat_duration:  # 75→70 BPM at 1:30
            beat_t = abs(current_second - 90.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        elif abs(current_second - 95.0) < heartbeat_duration:  # 70→60 BPM at 1:35
            beat_t = abs(current_second - 95.0) / heartbeat_duration
            heartbeat_scale = 1.0 + 0.15 * (1.0 - beat_t)
        
        # Apply heartbeat scale
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
            zoom_factor = 200 - 175 * phase_t  # Start very far, approach
            elevation = 20
            azimuth = 45
        
        # Phase 2 (10-25s): Energy burst, strings ascending
        elif current_second < 25.0:
            phase_t = (current_second - 10.0) / 15.0
            point_alpha = 0.8
            zoom_factor = 25 - 5 * phase_t  # Continue zooming in
            elevation = 20
            azimuth = 45 + 90 * phase_t
        
        # Phase 3 (25-40s): Strings coalesce, 80 BPM
        elif current_second < 40.0:
            phase_t = (current_second - 25.0) / 15.0
            point_alpha = 0.8
            zoom_factor = 20 - 3 * phase_t  # Continue zooming
            elevation = 20 + 10 * np.sin(np.pi * phase_t)
            azimuth = 135 + 90 * phase_t
        
        # Phase 4 (40-60s): Heartbeat rhythm, 85 BPM
        elif current_second < 60.0:
            phase_t = (current_second - 40.0) / 20.0
            point_alpha = 0.8
            zoom_factor = 17
            elevation = 20
            azimuth = 225 + 180 * phase_t
        
        # Phase 5 (60-75s): Majestic orchestral, 90 BPM
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 0.8
            zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 405 + 360 * phase_t
        
        # Phase 6 (75-90s): Cosmic expansion, 75 BPM
        elif current_second < 90.0:
            phase_t = (current_second - 75.0) / 15.0
            point_alpha = 0.8 + 0.2 * phase_t  # Glow effect
            zoom_factor = 20 + 80 * phase_t  # Zoom out dramatically
            elevation = 40 - 20 * phase_t
            azimuth = 585 + 90 * phase_t
        
        # Phase 7 (90-95s): Mathematical precision, 70 BPM
        elif current_second < 95.0:
            phase_t = (current_second - 90.0) / 5.0
            point_alpha = 1.0  # Fully bright
            zoom_factor = 100
            elevation = 20
            azimuth = 675
        
        # Phase 8 (95-100s): Fade to silence, 60 BPM, infinite stars
        else:
            phase_t = (current_second - 95.0) / 5.0
            point_alpha = 1.0 * (1.0 - phase_t)  # Fade out
            zoom_factor = 100 + 100 * phase_t
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
register_effect('H8', EffectH8)


"""
Effect H1: Heart Genesis (creation story - 100 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH1(BaseEffect):
    """Heart Genesis: creation story with particle formation."""
    
    def get_total_frames(self):
        return 3000  # 100 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Heart rotates slowly (180 degrees total)
        alpha_deg = frame * 180 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        point_alpha = 0.8
        
        # Phase 1 (0-10s): Empty black space with single point of light
        if current_second < 10.0:
            phase_t = current_second / 10.0
            point_alpha = 0.0  # Heart invisible
            zoom_factor = 200  # Very far
            elevation = 20
            azimuth = 45
            # Could add a single point of light here (would need additional scatter)
        
        # Phase 2 (10-25s): Point explodes into scattered particles forming heart shape
        elif current_second < 25.0:
            phase_t = (current_second - 10.0) / 15.0
            # Gradually reveal heart with particle-like effect (alpha fade in)
            point_alpha = 0.8 * phase_t
            # Scale from very small to normal
            scale = 0.1 + 0.9 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
            zoom_factor = 25 - 5 * phase_t  # Zoom in
            elevation = 20
            azimuth = 45
        
        # Phase 3 (25-40s): Particles coalesce, heart materializes with increasing density
        elif current_second < 40.0:
            phase_t = (current_second - 25.0) / 15.0
            point_alpha = 0.8
            zoom_factor = 20 - 3 * phase_t  # Continue zooming
            elevation = 20 + 10 * np.sin(np.pi * phase_t)
            azimuth = 45 + 90 * phase_t
        
        # Phase 4 (40-60s): Fully formed heart pulses to life (first heartbeat)
        elif current_second < 60.0:
            phase_t = (current_second - 40.0) / 20.0
            point_alpha = 0.8
            # Heartbeat pulse
            heartbeat = 1.0 + 0.2 * np.sin(2 * np.pi * 2 * phase_t) ** 2
            x_rotated = x_rotated * heartbeat
            y_rotated = y_rotated * heartbeat
            z_rotated = z_rotated * heartbeat
            zoom_factor = 17
            elevation = 20
            azimuth = 45 + 180 * phase_t
        
        # Phase 5 (60-75s): Heart rotates majestically, showing its beauty
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 0.8
            zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 225 + 360 * phase_t
        
        # Phase 6 (75-90s): Zoom out to cosmic scale, heart glows like a star
        elif current_second < 90.0:
            phase_t = (current_second - 75.0) / 15.0
            point_alpha = 0.8 + 0.2 * phase_t  # Glow effect (brighter)
            zoom_factor = 20 + 80 * phase_t  # Zoom out dramatically
            elevation = 40 - 20 * phase_t
            azimuth = 585 + 90 * phase_t
        
        # Phase 7 (90-95s): Fade formulas in as "blueprint of creation"
        elif current_second < 95.0:
            phase_t = (current_second - 90.0) / 5.0
            point_alpha = 1.0  # Fully bright
            zoom_factor = 100
            elevation = 20
            azimuth = 675
            # Formulas handled by show_formulas flag
        
        # Phase 8 (95-100s): Fade to infinite stars, one becomes the heart again
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
register_effect('H1', EffectH1)


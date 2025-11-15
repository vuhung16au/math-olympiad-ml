"""
Effect H3: Fractal Heart (recursive hearts - 90 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH3(BaseEffect):
    """Fractal Heart: recursive hearts within hearts."""
    
    def get_total_frames(self):
        return 2700  # 90 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Rotate main heart
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        point_alpha = 0.8
        
        # Phase 1 (0-15s): Start with normal heart
        if current_second < 15.0:
            zoom_factor = 20
            elevation = 20
            azimuth = 45 + 180 * (current_second / 15.0)
        
        # Phase 2 (15-45s): Zoom into heart center, discover smaller heart inside
        elif current_second < 45.0:
            phase_t = (current_second - 15.0) / 30.0
            # Zoom in dramatically
            zoom_factor = 20 - 18 * phase_t  # 20 to 2
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 225 + 360 * phase_t
            # Visual effect: scale down to show "inner heart"
            scale = 1.0 - 0.5 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
        
        # Phase 3 (45-60s): Zoom into that heart, find another (3-5 levels)
        elif current_second < 60.0:
            phase_t = (current_second - 45.0) / 15.0
            zoom_factor = 2 - 1.5 * phase_t  # 2 to 0.5
            elevation = 30 + 10 * np.sin(4 * np.pi * phase_t)
            azimuth = 585 + 360 * phase_t
            scale = 0.5 - 0.3 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
        
        # Phase 4 (60-75s): Zoom back out through all levels
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            zoom_factor = 0.5 + 19.5 * phase_t  # 0.5 to 20
            elevation = 40 - 20 * phase_t
            azimuth = 945 - 720 * phase_t
            scale = 0.2 + 0.8 * phase_t
            x_rotated = x_rotated * scale
            y_rotated = y_rotated * scale
            z_rotated = z_rotated * scale
        
        # Phase 5 (75-90s): Final reveal - the universe is made of hearts
        else:
            phase_t = (current_second - 75.0) / 15.0
            zoom_factor = 20 + 30 * phase_t  # Zoom out to cosmic scale
            elevation = 20
            azimuth = 225 + 180 * phase_t
            # Return to normal scale
            x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
            y_rotated = self.y_original
            z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H3', EffectH3)


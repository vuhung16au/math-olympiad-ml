"""
Effect H2: Time Reversal (forward then backward - 90 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH2(BaseEffect):
    """Time Reversal: forward then backward animation."""
    
    def get_total_frames(self):
        return 2700  # 90 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Phase 1 (0-45s): Normal G2-style journey forward
        if current_second < 45.0:
            phase_t = current_second / 45.0
            # Rotate heart
            alpha_deg = frame * 270 / (self.total_frames // 2)
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
            y_rotated = self.y_original
            z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
            
            # Camera motion
            zoom_factor = 20 - 10 * phase_t + 5 * np.sin(4 * np.pi * phase_t)
            elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 360 * phase_t
            point_alpha = 0.8
            
        # Phase 2 (45-48s): Freeze frame at peak moment
        elif current_second < 48.0:
            alpha_deg = (self.total_frames // 2) * 270 / (self.total_frames // 2)
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
            y_rotated = self.y_original
            z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
            
            zoom_factor = 15
            elevation = 35
            azimuth = 405
            point_alpha = 0.8
        
        # Phase 3 (48-90s): Reverse time - everything plays backward
        else:
            reverse_t = (current_second - 48.0) / 42.0
            reverse_frame = int((1.0 - reverse_t) * (self.total_frames // 2))
            
            # Rotate heart backward
            alpha_deg = reverse_frame * 270 / (self.total_frames // 2)
            alpha_rad = np.deg2rad(alpha_deg)
            x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
            y_rotated = self.y_original
            z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
            
            # Camera motion backward
            phase_t = 1.0 - reverse_t
            zoom_factor = 20 - 10 * phase_t + 5 * np.sin(4 * np.pi * phase_t)
            elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 360 * phase_t
            point_alpha = 0.8
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H2', EffectH2)


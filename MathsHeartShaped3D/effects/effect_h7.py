"""
Effect H7: Hologram Heart (wireframe tech aesthetic - 90 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH7(BaseEffect):
    """Hologram Heart: wireframe tech aesthetic."""
    
    def get_total_frames(self):
        return 2700  # 90 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Rotate heart
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        point_alpha = 0.8
        
        # Phase 1 (0-10s): Grid floor and walls appear (tron-style)
        if current_second < 10.0:
            phase_t = current_second / 10.0
            point_alpha = 0.0  # Heart invisible initially
            zoom_factor = 30
            elevation = 20
            azimuth = 45
        
        # Phase 2 (10-20s): Heart materializes as wireframe
        elif current_second < 20.0:
            phase_t = (current_second - 10.0) / 10.0
            point_alpha = 0.3 * phase_t  # Wireframe effect (low alpha)
            zoom_factor = 30 - 10 * phase_t
            elevation = 20
            azimuth = 45 + 90 * phase_t
        
        # Phase 3 (20-35s): Wireframe fills in with points progressively
        elif current_second < 35.0:
            phase_t = (current_second - 20.0) / 15.0
            point_alpha = 0.3 + 0.5 * phase_t  # Gradually fill
            zoom_factor = 20
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 135 + 180 * phase_t
        
        # Phase 4 (35-50s): Hologram "glitches" and reforms
        elif current_second < 50.0:
            phase_t = (current_second - 35.0) / 15.0
            # Glitch effect: random alpha fluctuations
            glitch = 0.1 * np.sin(20 * np.pi * phase_t) * np.sin(7 * np.pi * phase_t)
            point_alpha = 0.8 + glitch
            point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
            zoom_factor = 20 + 3 * np.sin(4 * np.pi * phase_t)
            elevation = 30 - 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 315 + 360 * phase_t
        
        # Phase 5 (50-70s): Multiple holographic layers (like x-ray views)
        elif current_second < 70.0:
            phase_t = (current_second - 50.0) / 20.0
            point_alpha = 0.8 + 0.2 * np.sin(2 * np.pi * phase_t)
            zoom_factor = 17 + 3 * np.sin(2 * np.pi * phase_t)
            elevation = 20 + 20 * np.sin(2 * np.pi * phase_t)
            azimuth = 675 + 540 * phase_t
        
        # Phase 6 (70-85s): Final solid form with scan lines effect
        elif current_second < 85.0:
            phase_t = (current_second - 70.0) / 15.0
            # Scan line effect: slight alpha variation
            scan_line = 0.1 * np.sin(10 * np.pi * phase_t)
            point_alpha = 1.0 + scan_line
            point_alpha = min(1.0, max(0.0, point_alpha))  # Clamp to 0-1
            zoom_factor = 20
            elevation = 40 - 20 * phase_t
            azimuth = 1215 + 180 * phase_t
        
        # Phase 7 (85-90s): Hologram powers down in sections
        else:
            phase_t = (current_second - 85.0) / 5.0
            point_alpha = 1.0 * (1.0 - phase_t)  # Fade out
            zoom_factor = 20 + 10 * phase_t
            elevation = 20
            azimuth = 1395
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H7', EffectH7)


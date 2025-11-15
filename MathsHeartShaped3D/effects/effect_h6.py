"""
Effect H6: Heart Nebula (cosmic space journey - 120 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH6(BaseEffect):
    """Heart Nebula: cosmic space journey."""
    
    def get_total_frames(self):
        return 3600  # 120 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Rotate heart slowly
        alpha_deg = frame * 180 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        point_alpha = 0.8
        
        # Phase 1 (0-15s): Start in deep space (distant heart glows like galaxy)
        if current_second < 15.0:
            phase_t = current_second / 15.0
            point_alpha = 0.3 + 0.5 * phase_t  # Glow effect
            zoom_factor = 200 - 150 * phase_t  # Very far to closer
            elevation = 20
            azimuth = 45
        
        # Phase 2 (15-45s): Travel through stars toward heart-nebula
        elif current_second < 45.0:
            phase_t = (current_second - 15.0) / 30.0
            point_alpha = 0.8 + 0.2 * np.sin(4 * np.pi * phase_t)  # Pulsing glow
            zoom_factor = 50 - 30 * phase_t  # Continue approaching
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 45 + 180 * phase_t
        
        # Phase 3 (45-60s): Pass through "cosmic dust" (particle effects)
        elif current_second < 60.0:
            phase_t = (current_second - 45.0) / 15.0
            point_alpha = 0.8 + 0.2 * np.sin(8 * np.pi * phase_t)  # Rapid pulsing
            zoom_factor = 20 - 5 * phase_t  # Get very close
            elevation = 30 - 10 * phase_t
            azimuth = 225 + 90 * phase_t
        
        # Phase 4 (60-75s): Arrive at heart, now massive and glowing
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 1.0  # Fully bright
            zoom_factor = 15 + 2 * np.sin(2 * np.pi * phase_t)
            elevation = 20 + 15 * np.sin(2 * np.pi * phase_t)
            azimuth = 315 + 180 * phase_t
        
        # Phase 5 (75-90s): Orbit around heart-planet
        elif current_second < 90.0:
            phase_t = (current_second - 75.0) / 15.0
            point_alpha = 1.0
            zoom_factor = 17
            elevation = 20 + 25 * np.sin(2 * np.pi * phase_t)
            azimuth = 495 + 360 * phase_t
        
        # Phase 6 (90-105s): See other "heart planets" in distance
        elif current_second < 105.0:
            phase_t = (current_second - 90.0) / 15.0
            point_alpha = 1.0
            zoom_factor = 17 + 20 * phase_t  # Zoom out to see others
            elevation = 45 - 25 * phase_t
            azimuth = 855 + 180 * phase_t
        
        # Phase 7 (105-120s): Zoom out - our heart is one of many in "heart galaxy"
        else:
            phase_t = (current_second - 105.0) / 15.0
            point_alpha = 1.0 - 0.2 * phase_t  # Slight fade
            zoom_factor = 37 + 163 * phase_t  # Zoom out dramatically
            elevation = 20
            azimuth = 1035 + 90 * phase_t
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H6', EffectH6)


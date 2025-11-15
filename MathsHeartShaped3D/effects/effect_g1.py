"""
Effect G1: Heart Journey (camera zooms through heart, then orbits back)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectG1(BaseEffect):
    """Heart Journey: camera zooms through heart, then orbits back."""
    
    def get_total_frames(self):
        return 2700  # 90 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Heart rotates slowly throughout (180 degrees over 90 seconds)
        alpha_deg = frame * 180 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Phase 1 (0-0.22): Rapid zoom approach through heart center (0-20 seconds)
        if t < 0.22:
            phase_t = t / 0.22
            # Zoom from far (150) to through center (-10), accelerating
            zoom_factor = 150 - 160 * (phase_t ** 2)
            # Slight elevation change for drama
            elevation = 10 + 10 * np.sin(np.pi * phase_t)
            azimuth = 45
            
        # Phase 2 (0.22-0.33): Exit and turnaround behind heart (20-30 seconds)
        elif t < 0.33:
            phase_t = (t - 0.22) / 0.11
            # Continue through to behind (-10 to 40)
            zoom_factor = -10 + 50 * phase_t
            elevation = 20
            # Swing around to opposite side (180 degrees)
            azimuth = 45 + 180 * phase_t
            
        # Phase 3 (0.33-1.0): Orbital return like moon (30-90 seconds, 2 complete orbits)
        else:
            phase_t = (t - 0.33) / 0.67
            # Gradually get closer (40 to 25)
            zoom_factor = 40 - 15 * phase_t
            # Elevation oscillates like orbital path (2 cycles)
            elevation = 20 + 25 * np.sin(2 * np.pi * 2 * phase_t)
            # 2 complete orbits (720 degrees)
            azimuth = 225 + 720 * phase_t
        
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('G1', EffectG1)


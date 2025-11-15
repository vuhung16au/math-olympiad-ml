"""
Effect G: Figure-8 Dance (rotation + figure-8 camera path)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectG(BaseEffect):
    """Figure-8 dance with lemniscate camera path."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Rotate heart around Y-axis
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Camera follows a figure-8 (lemniscate) path
        # Parametric equations for figure-8: x = sin(t), y = sin(t)*cos(t)
        azimuth_offset = 60 * np.sin(2 * np.pi * t)  # Horizontal figure-8 component
        elevation_offset = 30 * np.sin(4 * np.pi * t)  # Vertical figure-8 component (double frequency)
        
        azimuth = 45 + azimuth_offset + 180 * t  # Also slowly rotate around
        elevation = 20 + elevation_offset
        
        self.ax.view_init(elev=elevation, azim=azimuth)
        
        # Subtle zoom synchronized with figure-8 motion
        zoom_factor = 20 + 4 * np.sin(2 * np.pi * t)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('G', EffectG)


"""
Effect C: Combined (rotating heart + orbiting camera + zoom)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectC(BaseEffect):
    """Combined effects: rotating heart + orbiting camera + zoom."""
    
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
        
        # Camera orbits slower (180 degrees total)
        azimuth = 45 + 180 * t
        elevation = 20 + 15 * np.sin(np.pi * t)
        self.ax.view_init(elev=elevation, azim=azimuth)
        
        # Zoom effect: zoom in first half, zoom out second half
        if t < 0.5:
            zoom_factor = 20 - 5 * (t * 2)  # Zoom in from 20 to 15
        else:
            zoom_factor = 15 + 5 * ((t - 0.5) * 2)  # Zoom out from 15 to 20
        
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('C', EffectC)


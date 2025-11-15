"""
Effect F: Spiral Ascent (rotation + spiral camera + zoom out)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectF(BaseEffect):
    """Spiral ascent with camera spiraling upward."""
    
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
        
        # Camera spirals upward while orbiting
        azimuth = 45 + 720 * t  # Two full rotations
        elevation = -10 + 70 * t  # Rises from -10 to 60 degrees
        self.ax.view_init(elev=elevation, azim=azimuth)
        
        # Gradual zoom out as camera ascends
        zoom_factor = 20 + 15 * t  # Zoom from 20 to 35
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('F', EffectF)


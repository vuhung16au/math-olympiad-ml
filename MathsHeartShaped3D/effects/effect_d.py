"""
Effect D: Custom (Y rotation + elevation sweep + zoom pulse)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectD(BaseEffect):
    """Custom animation with elevation sweep and zoom pulse."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Rotate around Y-axis
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Smooth elevation sweep from bottom to top and back
        elevation = 20 + 40 * np.sin(np.pi * t)
        self.ax.view_init(elev=elevation, azim=45)
        
        # Subtle zoom pulse
        zoom_factor = 20 + 3 * np.sin(4 * np.pi * t)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('D', EffectD)


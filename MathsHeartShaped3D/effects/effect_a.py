"""
Effect A: Multi-axis rotation (Y-axis + X-axis wobble)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectA(BaseEffect):
    """Multi-axis rotation with gentle X-axis wobble."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Primary rotation around Y-axis
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        # Add gentle X-axis wobble (15-degree amplitude)
        beta_deg = 15 * np.sin(2 * np.pi * t)
        beta_rad = np.deg2rad(beta_deg)
        
        # Rotate around Y-axis first
        x_temp = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_temp = self.y_original
        z_temp = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Then rotate around X-axis for wobble
        x_rotated = x_temp
        y_rotated = y_temp * np.cos(beta_rad) - z_temp * np.sin(beta_rad)
        z_rotated = y_temp * np.sin(beta_rad) + z_temp * np.cos(beta_rad)
        
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        return self.scatter,


# Register the effect
register_effect('A', EffectA)


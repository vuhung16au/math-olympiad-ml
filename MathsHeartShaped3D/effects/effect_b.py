"""
Effect B: Dynamic camera orbit (heart stays stationary)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectB(BaseEffect):
    """Dynamic camera orbit around stationary heart."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Heart doesn't rotate
        self.scatter._offsets3d = (self.x_original, self.y_original, self.z_original)
        
        # Camera orbits around the heart
        azimuth = 45 + 360 * t
        elevation = 20 + 20 * np.sin(2 * np.pi * t)  # Elevation oscillates
        self.ax.view_init(elev=elevation, azim=azimuth)
        
        return self.scatter,


# Register the effect
register_effect('B', EffectB)


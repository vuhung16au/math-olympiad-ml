"""
Effect E: Heartbeat Pulse (rotation + rhythmic scaling)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectE(BaseEffect):
    """Heartbeat pulse with rhythmic scaling."""
    
    def get_total_frames(self):
        return 900  # 30 seconds at 30 fps
    
    def update(self, frame):
        # Calculate normalized time (0 to 1)
        t = self.get_normalized_time(frame)
        
        # Rotate around Y-axis
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_temp = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_temp = self.y_original
        z_temp = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Heartbeat pulse: double beat pattern (lub-dub)
        # Create a heartbeat rhythm with two pulses per cycle
        heartbeat_freq = 2  # 2 beats per rotation
        pulse1 = np.sin(2 * np.pi * heartbeat_freq * t) ** 2
        pulse2 = np.sin(2 * np.pi * heartbeat_freq * t + np.pi/3) ** 2
        heartbeat = 1.0 + 0.15 * (pulse1 + 0.5 * pulse2)  # Scale between 1.0 and 1.15
        
        # Apply pulsating scale
        x_rotated = x_temp * heartbeat
        y_rotated = y_temp * heartbeat
        z_rotated = z_temp * heartbeat
        
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        # Gentle camera wobble synchronized with heartbeat
        elevation = 20 + 5 * np.sin(2 * np.pi * heartbeat_freq * t)
        self.ax.view_init(elev=elevation, azim=45)
        
        return self.scatter,


# Register the effect
register_effect('E', EffectE)


"""
Effect H5: Kaleidoscope Heart (mirrored reflections - 60 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH5(BaseEffect):
    """Kaleidoscope Heart: mirrored reflections creating patterns."""
    
    def get_total_frames(self):
        return 1800  # 60 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Rotate heart
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        point_alpha = 0.8
        
        # Phase 1 (0-10s): Single heart in center
        if current_second < 10.0:
            zoom_factor = 20
            elevation = 20
            azimuth = 45 + 180 * (current_second / 10.0)
        
        # Phase 2 (10-25s): Mirrors appear (4 quadrants)
        elif current_second < 25.0:
            phase_t = (current_second - 10.0) / 15.0
            # Create 4 mirrored hearts
            x_all = np.concatenate([
                x_rotated,  # Original
                -x_rotated,  # Mirror X
                x_rotated,  # Mirror Y
                -x_rotated,  # Mirror both
            ])
            y_all = np.concatenate([y_rotated, y_rotated, -y_rotated, -y_rotated])
            z_all = np.concatenate([z_rotated, -z_rotated, z_rotated, -z_rotated])
            
            # Fade in mirrors
            if phase_t < 0.5:
                point_alpha = 0.8 * (phase_t * 2)
            else:
                point_alpha = 0.8
            
            x_rotated = x_all
            y_rotated = y_all
            z_rotated = z_all
            zoom_factor = 25
            elevation = 20
            azimuth = 225 + 180 * phase_t
        
        # Phase 3 (25-40s): 8 mirrors (add diagonal)
        elif current_second < 40.0:
            phase_t = (current_second - 25.0) / 15.0
            # 8 hearts in octagon pattern
            angles = np.linspace(0, 2*np.pi, 8, endpoint=False)
            x_all = []
            y_all = []
            z_all = []
            for angle in angles:
                cos_a = np.cos(angle)
                sin_a = np.sin(angle)
                x_mirror = x_rotated * cos_a - z_rotated * sin_a
                z_mirror = x_rotated * sin_a + z_rotated * cos_a
                x_all.append(x_mirror)
                y_all.append(y_rotated)
                z_all.append(z_mirror)
            
            x_rotated = np.concatenate(x_all)
            y_rotated = np.concatenate(y_all)
            z_rotated = np.concatenate(z_all)
            zoom_factor = 30
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 405 + 360 * phase_t
        
        # Phase 4 (40-50s): 16 mirrors (mandala pattern)
        elif current_second < 50.0:
            phase_t = (current_second - 40.0) / 10.0
            # 16 hearts
            angles = np.linspace(0, 2*np.pi, 16, endpoint=False)
            x_all = []
            y_all = []
            z_all = []
            for angle in angles:
                cos_a = np.cos(angle)
                sin_a = np.sin(angle)
                x_mirror = x_rotated * cos_a - z_rotated * sin_a
                z_mirror = x_rotated * sin_a + z_rotated * cos_a
                x_all.append(x_mirror)
                y_all.append(y_rotated)
                z_all.append(z_mirror)
            
            x_rotated = np.concatenate(x_all)
            y_rotated = np.concatenate(y_all)
            z_rotated = np.concatenate(z_all)
            zoom_factor = 35
            elevation = 20 + 15 * np.sin(4 * np.pi * phase_t)
            azimuth = 765 + 720 * phase_t
        
        # Phase 5 (50-55s): Pattern collapses back to single heart
        elif current_second < 55.0:
            phase_t = (current_second - 50.0) / 5.0
            point_alpha = 0.8 * (1.0 - phase_t)
            zoom_factor = 35 - 15 * phase_t
            elevation = 35 - 15 * phase_t
            azimuth = 1485 - 1440 * phase_t
        
        # Phase 6 (55-60s): Final reveal - was always one heart
        else:
            phase_t = (current_second - 55.0) / 5.0
            point_alpha = 0.8 * phase_t
            zoom_factor = 20
            elevation = 20
            azimuth = 45
            # Reset to single heart
            x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
            y_rotated = self.y_original
            z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H5', EffectH5)


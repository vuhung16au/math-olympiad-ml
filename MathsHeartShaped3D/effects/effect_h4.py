"""
Effect H4: Dual Hearts (two hearts dancing - 120 seconds)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectH4(BaseEffect):
    """Dual Hearts: two hearts dancing together."""
    
    def __init__(self, total_frames, fps, x_original, y_original, z_original, 
                 scatter, ax, audio_features=None, x_heart2=None, y_heart2=None, z_heart2=None):
        """Initialize with second heart coordinates."""
        super().__init__(total_frames, fps, x_original, y_original, z_original, 
                        scatter, ax, audio_features)
        self.x_heart2 = x_heart2 if x_heart2 is not None else x_original
        self.y_heart2 = y_heart2 if y_heart2 is not None else y_original
        self.z_heart2 = z_heart2 if z_heart2 is not None else z_original
    
    def get_total_frames(self):
        return 3600  # 120 seconds at 30 fps
    
    def update(self, frame):
        current_second = self.get_current_second(frame)
        
        # Rotate both hearts
        alpha_deg = frame * 360 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        # Heart 1 (original)
        x1 = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y1 = self.y_original
        z1 = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Heart 2 (offset and rotated)
        x2 = self.x_heart2 * np.cos(alpha_rad + np.pi/4) + self.z_heart2 * np.sin(alpha_rad + np.pi/4)
        y2 = self.y_heart2
        z2 = -self.x_heart2 * np.sin(alpha_rad + np.pi/4) + self.z_heart2 * np.cos(alpha_rad + np.pi/4)
        
        # Phase 1 (0-15s): First heart appears
        if current_second < 15.0:
            phase_t = current_second / 15.0
            # Only show heart 1, fade in
            point_alpha = 0.8 * phase_t
            # Position heart 1
            offset = 0
            x_rotated = x1 + offset
            y_rotated = y1
            z_rotated = z1
            zoom_factor = 30 - 10 * phase_t
            elevation = 20
            azimuth = 45
        
        # Phase 2 (15-30s): Second heart appears
        elif current_second < 30.0:
            phase_t = (current_second - 15.0) / 15.0
            point_alpha = 0.8
            # Combine both hearts with offset
            offset1 = -8 * (1.0 - phase_t)
            offset2 = 8 * phase_t
            x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1, z2])
            zoom_factor = 20
            elevation = 20
            azimuth = 45 + 90 * phase_t
        
        # Phase 3 (30-60s): Hearts orbit each other like binary stars
        elif current_second < 60.0:
            phase_t = (current_second - 30.0) / 30.0
            point_alpha = 0.8
            orbit_radius = 8
            angle = 2 * np.pi * phase_t
            offset1 = orbit_radius * np.cos(angle)
            offset2 = orbit_radius * np.cos(angle + np.pi)
            x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
            zoom_factor = 25
            elevation = 20 + 10 * np.sin(2 * np.pi * phase_t)
            azimuth = 135 + 360 * phase_t
        
        # Phase 4 (60-75s): Hearts spiral closer
        elif current_second < 75.0:
            phase_t = (current_second - 60.0) / 15.0
            point_alpha = 0.8
            orbit_radius = 8 * (1.0 - phase_t)  # Spiral in
            angle = 2 * np.pi * phase_t * 2
            offset1 = orbit_radius * np.cos(angle)
            offset2 = orbit_radius * np.cos(angle + np.pi)
            x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
            zoom_factor = 20 - 5 * phase_t
            elevation = 30 - 10 * phase_t
            azimuth = 495 + 180 * phase_t
        
        # Phase 5 (75-85s): Hearts briefly merge/overlap
        elif current_second < 85.0:
            phase_t = (current_second - 75.0) / 10.0
            point_alpha = 0.8 + 0.2 * np.sin(4 * np.pi * phase_t)  # Pulse
            # Hearts at same position
            x_rotated = np.concatenate([x1, x2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1, z2])
            zoom_factor = 15
            elevation = 20
            azimuth = 675 + 90 * phase_t
        
        # Phase 6 (85-95s): Hearts separate but remain connected by "thread"
        elif current_second < 95.0:
            phase_t = (current_second - 85.0) / 10.0
            point_alpha = 0.8
            separation = 4 * phase_t
            x_rotated = np.concatenate([x1 - separation, x2 + separation])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1, z2])
            zoom_factor = 15 + 5 * phase_t
            elevation = 20
            azimuth = 765 + 90 * phase_t
        
        # Phase 7 (95-105s): Final orbit, synchronized rotation
        elif current_second < 105.0:
            phase_t = (current_second - 95.0) / 10.0
            point_alpha = 0.8
            orbit_radius = 4 + 4 * phase_t
            angle = 2 * np.pi * phase_t
            offset1 = orbit_radius * np.cos(angle)
            offset2 = orbit_radius * np.cos(angle + np.pi)
            x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
            zoom_factor = 20
            elevation = 20 + 5 * np.sin(4 * np.pi * phase_t)
            azimuth = 855 + 360 * phase_t
        
        # Phase 8 (105-120s): Fade to black, showing connection line last
        else:
            phase_t = (current_second - 105.0) / 15.0
            point_alpha = 0.8 * (1.0 - phase_t)
            orbit_radius = 8
            angle = 2 * np.pi * (1.0 + phase_t)
            offset1 = orbit_radius * np.cos(angle)
            offset2 = orbit_radius * np.cos(angle + np.pi)
            x_rotated = np.concatenate([x1 + offset1, x2 + offset2])
            y_rotated = np.concatenate([y1, y2])
            z_rotated = np.concatenate([z1 + orbit_radius * np.sin(angle), z2 + orbit_radius * np.sin(angle + np.pi)])
            zoom_factor = 20 + 10 * phase_t
            elevation = 25
            azimuth = 1215
        
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('H4', EffectH4)


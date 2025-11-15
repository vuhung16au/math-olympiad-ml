"""
Effect G2: Epic Heart Story (137 seconds total - 4110 frames)
"""

import numpy as np
from effects import BaseEffect, register_effect


class EffectG2(BaseEffect):
    """Epic Heart Story: multi-phase journey with fade in/out and formulas."""
    
    def get_total_frames(self):
        return 4110  # 137 seconds at 30 fps
    
    def update(self, frame):
        # Convert frame to seconds for easier calculation
        current_second = self.get_current_second(frame)
        
        # Heart rotates throughout entire animation (slower - 270 degrees total)
        alpha_deg = frame * 270 / self.total_frames
        alpha_rad = np.deg2rad(alpha_deg)
        
        x_rotated = self.x_original * np.cos(alpha_rad) + self.z_original * np.sin(alpha_rad)
        y_rotated = self.y_original
        z_rotated = -self.x_original * np.sin(alpha_rad) + self.z_original * np.cos(alpha_rad)
        
        # Default alpha for heart points
        point_alpha = 0.8
        
        # Phase 1 (0-1s): Fade in from black
        if current_second < 1.0:
            point_alpha = current_second  # 0 to 1
            zoom_factor = 12  # Changed from 25 to 12 (heart 2x bigger)
            elevation = 20
            azimuth = 45
            
        # Phase 2 (1-3s): Gradually show heart with G1 starting position
        elif current_second < 3.0:
            phase_t = (current_second - 1.0) / 2.0
            point_alpha = 0.8
            zoom_factor = 80 - 68 * phase_t  # 80 to 12 (closer for larger heart)
            elevation = 10 + 10 * phase_t  # 10 to 20
            azimuth = 45
            
        # Phase 3 (3-60s): Run G1 effect (first 57 seconds of it - condensed)
        elif current_second < 60.0:
            phase_t = (current_second - 3.0) / 57.0  # Normalize to 0-1
            point_alpha = 0.8
            
            # Condensed G1: zoom through, turn, and start orbit
            if phase_t < 0.35:  # 0-20s: Zoom through
                sub_t = phase_t / 0.35
                zoom_factor = 12 - 22 * (sub_t ** 2)  # 12 to -10 (through heart, larger)
                elevation = 20 + 5 * np.sin(np.pi * sub_t)
                azimuth = 45
            elif phase_t < 0.53:  # 20-30s: Exit and turn
                sub_t = (phase_t - 0.35) / 0.18
                zoom_factor = -10 + 22 * sub_t  # -10 to 12 (adjusted)
                elevation = 20
                azimuth = 45 + 180 * sub_t
            else:  # 30-60s: Start orbital motion
                sub_t = (phase_t - 0.53) / 0.47
                zoom_factor = 12 - 2 * sub_t  # 12 to 10 (closer orbit)
                elevation = 20 + 20 * np.sin(2 * np.pi * sub_t)
                azimuth = 225 + 360 * sub_t
                
        # Phase 4 (60-62s): Fade out heart
        elif current_second < 62.0:
            phase_t = (current_second - 60.0) / 2.0
            point_alpha = 0.8 * (1.0 - phase_t)  # 0.8 to 0
            zoom_factor = 10  # Changed from 20 to 10
            elevation = 20
            azimuth = 225 + 360 * 0.53
            
        # Phase 5 (62-64s): Black screen with formulas (heart invisible)
        elif current_second < 64.0:
            point_alpha = 0.0  # Heart invisible
            zoom_factor = 10  # Changed from 20 to 10
            elevation = 20
            azimuth = 45
            # Formula display handled by setup_figure, just keep heart hidden
            
        # Phase 6 (64-66s): Fade formulas out (keep heart hidden, formulas handled by matplotlib text alpha)
        elif current_second < 66.0:
            point_alpha = 0.0  # Heart still invisible
            zoom_factor = 10  # Changed from 20 to 10
            elevation = 20
            azimuth = 45
            
        # Phase 7 (66-68s): Fade heart back in at G1 starting position
        elif current_second < 68.0:
            phase_t = (current_second - 66.0) / 2.0
            point_alpha = 0.8 * phase_t  # 0 to 0.8
            zoom_factor = 30  # Changed from 50 to 30 (closer start)
            elevation = 15
            azimuth = 45
            
        # Phase 8 (68-90s): Zoom through heart (accelerated)
        elif current_second < 90.0:
            phase_t = (current_second - 68.0) / 22.0
            point_alpha = 0.8
            zoom_factor = 30 - 50 * (phase_t ** 1.5)  # 30 to -20 (adjusted range)
            elevation = 15 + 15 * np.sin(np.pi * phase_t)
            azimuth = 45 + 90 * phase_t
            
        # Phase 9 (90-92s): Exit and show heart from behind
        elif current_second < 92.0:
            phase_t = (current_second - 90.0) / 2.0
            point_alpha = 0.8
            zoom_factor = -20 + 35 * phase_t  # -20 to 15 (closer)
            elevation = 30
            azimuth = 135 + 90 * phase_t  # Complete the turn
            
        # Phase 10 (92-102s): Slow zoom out, heart gets smaller
        elif current_second < 102.0:
            phase_t = (current_second - 92.0) / 10.0
            point_alpha = 0.8
            zoom_factor = 15 + 50 * phase_t  # 15 to 65 (not as far)
            elevation = 30 - 10 * phase_t  # Slowly descend
            azimuth = 225 + 180 * phase_t
            
        # Phase 11 (102-122s): Zoom back in dramatically
        elif current_second < 122.0:
            phase_t = (current_second - 102.0) / 20.0
            point_alpha = 0.8
            # Dramatic zoom: 65 down to 10 (very close)
            zoom_factor = 65 - 55 * (phase_t ** 2)  # Accelerating zoom in
            elevation = 20 + 25 * np.sin(np.pi * phase_t)  # Dramatic arc
            azimuth = 405 + 270 * phase_t  # Continue orbit
            
        # Phase 12 (122-132s): Moon orbit around heart
        elif current_second < 132.0:
            phase_t = (current_second - 122.0) / 10.0
            point_alpha = 0.8
            zoom_factor = 10 + 4 * np.sin(2 * np.pi * phase_t)  # Closer orbit (10±4)
            elevation = 25 + 15 * np.sin(2 * np.pi * 2 * phase_t)  # 2 oscillations
            azimuth = 675 + 720 * phase_t  # 2 complete orbits
            
        # Phase 13 (132-137s): Quick zoom out and fade to black
        elif current_second < 137.0:
            phase_t = (current_second - 132.0) / 5.0
            point_alpha = 0.8 * (1.0 - phase_t)  # Fade out: 0.8 to 0
            zoom_factor = 10 + 60 * (phase_t ** 2)  # 10 to 70 (less dramatic)
            elevation = 25 - 25 * phase_t  # Return to neutral
            azimuth = 1395 + 180 * phase_t
        
        else:
            # Fallback (shouldn't reach here)
            point_alpha = 0.0
            zoom_factor = 10  # Changed from 20 to 10
            elevation = 20
            azimuth = 45
        
        # Apply alpha and position
        self.scatter.set_alpha(point_alpha)
        self.scatter._offsets3d = (x_rotated, y_rotated, z_rotated)
        
        self.ax.view_init(elev=elevation, azim=azimuth)
        self.ax.set_xlim([-zoom_factor, zoom_factor])
        self.ax.set_ylim([-zoom_factor, zoom_factor])
        self.ax.set_zlim([-zoom_factor, zoom_factor])
        
        return self.scatter,


# Register the effect
register_effect('G2', EffectG2)


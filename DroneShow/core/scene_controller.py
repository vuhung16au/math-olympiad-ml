"""
Scene Controller
Manages timeline, scene transitions, and drone formations throughout the show.
"""

import numpy as np
from config.drone_config import (
    SCENES, FPS, TRANSITION_DURATION,
    HEART_DRONES, STAR_DRONES,
    VIETNAM_DRONES, AUSTRALIA_DRONES,
    I_LOVE_VIETNAM_DRONES, I_LOVE_AUSTRALIA_DRONES,
    VIETNAM_COLOR_TOP, VIETNAM_COLOR_BOTTOM,
    AUSTRALIA_COLOR_TOP, AUSTRALIA_COLOR_BOTTOM,
    TOTAL_DRONES
)
from core.shape_generators import (
    generate_heart_formation,
    generate_star_formation,
    generate_text_formation,
    generate_combined_text_formation,
    generate_parking_grid
)


class Scene:
    """
    Represents a single scene in the show.
    """
    
    def __init__(self, name, duration, formation_generator, **kwargs):
        """
        Initialize a scene.
        
        Args:
            name: Scene identifier
            duration: Duration in seconds
            formation_generator: Function to generate (positions, colors)
            **kwargs: Additional parameters for formation generator
        """
        self.name = name
        self.duration = duration
        self.formation_generator = formation_generator
        self.kwargs = kwargs
        self.positions = None
        self.colors = None
    
    def generate_formation(self):
        """Generate the formation for this scene."""
        if self.positions is None:
            self.positions, self.colors = self.formation_generator(**self.kwargs)
        return self.positions, self.colors


class SceneController:
    """
    Controls the sequence of scenes and transitions.
    """
    
    def __init__(self, mode='testing', fps=FPS):
        """
        Initialize scene controller.
        
        Args:
            mode: 'testing' or 'production'
            fps: Frames per second
        """
        self.mode = mode
        self.fps = fps
        self.scenes = []
        self.current_scene_index = 0
        self.current_time = 0.0
        
        self._setup_scenes()
    
    def _setup_scenes(self):
        """Setup all scenes based on mode."""
        duration_key = f'duration_{self.mode}'
        
        # Scene 0: Blackout start
        self.scenes.append(Scene(
            'blackout_start',
            SCENES[0][duration_key],
            self._generate_blackout
        ))
        
        # Scene 1: Heart
        self.scenes.append(Scene(
            'heart',
            SCENES[1][duration_key],
            generate_heart_formation,
            num_drones=HEART_DRONES
        ))
        
        # Scene 2: Star
        self.scenes.append(Scene(
            'star',
            SCENES[2][duration_key],
            generate_star_formation,
            num_drones=STAR_DRONES
        ))
        
        # Scene 3: VIETNAM
        self.scenes.append(Scene(
            'vietnam',
            SCENES[3][duration_key],
            generate_text_formation,
            text='VIETNAM',
            num_drones=VIETNAM_DRONES,
            color_top=VIETNAM_COLOR_TOP,
            color_bottom=VIETNAM_COLOR_BOTTOM
        ))
        
        # Scene 4: AUSTRALIA
        self.scenes.append(Scene(
            'australia',
            SCENES[4][duration_key],
            generate_text_formation,
            text='AUSTRALIA',
            num_drones=AUSTRALIA_DRONES,
            color_top=AUSTRALIA_COLOR_TOP,
            color_bottom=AUSTRALIA_COLOR_BOTTOM
        ))
        
        # Scene 5: I ❤ VIETNAM
        self.scenes.append(Scene(
            'i_love_vietnam',
            SCENES[5][duration_key],
            generate_combined_text_formation,
            prefix='I',
            text_body='VIETNAM',
            emoji_drones=100,
            color_top=VIETNAM_COLOR_TOP,
            color_bottom=VIETNAM_COLOR_BOTTOM
        ))
        
        # Scene 6: I ❤ AUSTRALIA
        self.scenes.append(Scene(
            'i_love_australia',
            SCENES[6][duration_key],
            generate_combined_text_formation,
            prefix='I',
            text_body='AUSTRALIA',
            emoji_drones=100,
            color_top=AUSTRALIA_COLOR_TOP,
            color_bottom=AUSTRALIA_COLOR_BOTTOM
        ))
        
        # Scene 7: Blackout end
        self.scenes.append(Scene(
            'blackout_end',
            SCENES[7][duration_key],
            self._generate_blackout
        ))
    
    def _generate_blackout(self):
        """Generate blackout formation (all drones parked, lights off)."""
        return generate_parking_grid(TOTAL_DRONES, used_drones=0)
    
    def get_total_duration(self):
        """Get total show duration in seconds."""
        return sum(scene.duration for scene in self.scenes)
    
    def get_total_frames(self):
        """Get total number of frames."""
        return int(self.get_total_duration() * self.fps)
    
    def get_scene_at_time(self, time):
        """
        Get scene active at given time.
        
        Args:
            time: Time in seconds
        
        Returns:
            scene_index, scene_time (time within scene)
        """
        elapsed = 0.0
        for i, scene in enumerate(self.scenes):
            if elapsed + scene.duration > time:
                return i, time - elapsed
            elapsed += scene.duration
        
        # Past end, return last scene
        return len(self.scenes) - 1, 0.0
    
    def get_formation_at_time(self, time):
        """
        Get drone formation (positions and colors) at given time.
        Handles transitions between scenes.
        
        Args:
            time: Time in seconds
        
        Returns:
            positions: numpy array of shape (N, 3)
            colors: numpy array of shape (N, 3)
        """
        scene_idx, scene_time = self.get_scene_at_time(time)
        
        # Check if we're in a transition
        if scene_time < TRANSITION_DURATION and scene_idx > 0:
            # Transitioning from previous scene
            prev_scene = self.scenes[scene_idx - 1]
            curr_scene = self.scenes[scene_idx]
            
            # Generate both formations
            prev_pos, prev_colors = prev_scene.generate_formation()
            curr_pos, curr_colors = curr_scene.generate_formation()
            
            # Interpolate
            t = scene_time / TRANSITION_DURATION
            positions, colors = self._interpolate_formations(
                prev_pos, prev_colors,
                curr_pos, curr_colors,
                t
            )
        elif scene_time > (self.scenes[scene_idx].duration - TRANSITION_DURATION) and \
             scene_idx < len(self.scenes) - 1:
            # Transitioning to next scene
            curr_scene = self.scenes[scene_idx]
            next_scene = self.scenes[scene_idx + 1]
            
            # Generate both formations
            curr_pos, curr_colors = curr_scene.generate_formation()
            next_pos, next_colors = next_scene.generate_formation()
            
            # Interpolate
            t = (scene_time - (curr_scene.duration - TRANSITION_DURATION)) / TRANSITION_DURATION
            positions, colors = self._interpolate_formations(
                curr_pos, curr_colors,
                next_pos, next_colors,
                t
            )
        else:
            # Steady state within scene
            positions, colors = self.scenes[scene_idx].generate_formation()
        
        # Ensure we have exactly TOTAL_DRONES positions/colors
        positions, colors = self._pad_or_trim_formation(positions, colors)
        
        return positions, colors
    
    def _interpolate_formations(self, pos1, colors1, pos2, colors2, t):
        """
        Interpolate between two formations with easing.
        
        Args:
            pos1, colors1: First formation
            pos2, colors2: Second formation
            t: Interpolation factor (0-1)
        
        Returns:
            Interpolated positions and colors
        """
        # Apply ease-in-ease-out to t
        if t < 0.5:
            t_eased = 2 * t * t
        else:
            t_eased = 1 - 2 * (1 - t) ** 2
        
        # Ensure both formations have exactly TOTAL_DRONES
        pos1, colors1 = self._pad_or_trim_formation(pos1, colors1)
        pos2, colors2 = self._pad_or_trim_formation(pos2, colors2)
        
        # Interpolate
        positions = pos1 + t_eased * (pos2 - pos1)
        colors = colors1 + t_eased * (colors2 - colors1)
        colors = np.round(colors).astype(int)
        colors = np.clip(colors, 0, 255)
        
        return positions, colors
    
    def _pad_or_trim_formation(self, positions, colors):
        """
        Ensure formation has exactly TOTAL_DRONES drones.
        
        Args:
            positions: numpy array
            colors: numpy array
        
        Returns:
            Padded/trimmed positions and colors
        """
        # Ensure both arrays have same length
        num_pos = len(positions)
        num_colors = len(colors)
        
        if num_pos != num_colors:
            # Take minimum to be safe
            min_len = min(num_pos, num_colors)
            positions = positions[:min_len]
            colors = colors[:min_len]
        
        num_current = len(positions)
        
        if num_current < TOTAL_DRONES:
            # Need to add parking drones
            parking_pos, parking_colors = generate_parking_grid(
                TOTAL_DRONES, num_current
            )
            positions = np.vstack([positions, parking_pos])
            colors = np.vstack([colors, parking_colors])
        elif num_current > TOTAL_DRONES:
            # Trim excess
            positions = positions[:TOTAL_DRONES]
            colors = colors[:TOTAL_DRONES]
        
        return positions, colors
    
    def get_scene_info(self):
        """
        Get information about all scenes.
        
        Returns:
            List of dicts with scene information
        """
        info = []
        elapsed = 0.0
        
        for scene in self.scenes:
            info.append({
                'name': scene.name,
                'start_time': elapsed,
                'end_time': elapsed + scene.duration,
                'duration': scene.duration
            })
            elapsed += scene.duration
        
        return info


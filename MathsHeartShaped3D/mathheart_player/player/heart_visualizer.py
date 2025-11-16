"""
Heart Visualizer Module for MathHeart Player
Adapts existing heart effects for real-time rendering
"""

import os
import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D
from typing import Optional, Dict, Tuple

# Add parent directory to path to import existing modules
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core.heart_generator import generate_heart_points
from effects import get_effect_class
from mathheart_player.player.audio_analyzer import AudioAnalyzer

logger = logging.getLogger(__name__)


class HeartVisualizer:
    """Real-time 3D heart visualizer adapted from existing effects."""
    
    def __init__(self, canvas, effect_name: str = 'H8sync', density: str = 'lower'):
        """
        Initialize heart visualizer.
        
        Parameters:
            canvas: Matplotlib canvas widget
            effect_name: Effect name (H8sync, H9, H10)
            density: Point density ('lower', 'low', 'medium', 'high')
        """
        logger.info(f"Initializing HeartVisualizer: effect={effect_name}, density={density}")
        
        self.canvas = canvas
        self.effect_name = effect_name
        self.density = density
        self.fps = 30
        
        # Setup figure and axes
        self.fig = canvas.figure
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('black')
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
        logger.debug("Generating heart points")
        # Generate heart points
        self.x_original, self.y_original, self.z_original, _ = generate_heart_points(
            u_points=200, v_points=200, density=density
        )
        
        # Create scatter plot
        self.scatter = self.ax.scatter(
            self.x_original, self.y_original, self.z_original,
            c='red', s=1, alpha=0.8
        )
        
        # Effect instance (will be created when audio is loaded)
        self.effect_instance = None
        self.audio_features = None
        self.current_time = 0.0
        self.duration = 0.0
        
        # For H4 effect (dual hearts)
        self.x_heart2 = None
        self.y_heart2 = None
        self.z_heart2 = None
        
    def set_effect(self, effect_name: str):
        """
        Set visualization effect.
        
        Parameters:
            effect_name: Effect name (H8sync, H9, H10)
        """
        logger.info(f"Setting visualization effect: {self.effect_name} -> {effect_name}")
        self.effect_name = effect_name
        self._create_effect_instance()
    
    def load_audio_features(self, audio_analyzer: AudioAnalyzer):
        """
        Load audio features from analyzer.
        
        Parameters:
            audio_analyzer: AudioAnalyzer instance
        """
        logger.debug("Loading audio features into visualizer")
        self.audio_features = audio_analyzer.get_all_features()
        self.duration = audio_analyzer.get_duration()
        logger.debug(f"Audio features loaded: duration={self.duration:.2f}s")
        self._create_effect_instance()
    
    def _create_effect_instance(self):
        """Create effect instance based on current settings."""
        logger.debug(f"Creating effect instance: {self.effect_name}")
        EffectClass = get_effect_class(self.effect_name)
        if EffectClass is None:
            logger.warning(f"Effect '{self.effect_name}' not found")
            self.effect_instance = None
            return
        
        # Calculate total frames based on duration
        if self.duration > 0:
            total_frames = int(self.duration * self.fps)
        else:
            # Default duration if not set
            total_frames = 3000  # 100 seconds at 30 fps
        
        # For H4 effect, need second heart
        if self.effect_name == 'H4':
            if self.x_heart2 is None:
                logger.debug("Generating second heart for H4 effect")
                self.x_heart2, self.y_heart2, self.z_heart2, _ = generate_heart_points(
                    u_points=200, v_points=200, density=self.density
                )
            
            try:
                self.effect_instance = EffectClass(
                    total_frames=total_frames,
                    fps=self.fps,
                    x_original=self.x_original,
                    y_original=self.y_original,
                    z_original=self.z_original,
                    scatter=self.scatter,
                    ax=self.ax,
                    audio_features=self.audio_features,
                    x_heart2=self.x_heart2,
                    y_heart2=self.y_heart2,
                    z_heart2=self.z_heart2
                )
                logger.debug(f"H4 effect instance created: total_frames={total_frames}")
            except Exception as e:
                logger.error(f"Failed to create H4 effect instance: {e}", exc_info=True)
                self.effect_instance = None
        else:
            try:
                self.effect_instance = EffectClass(
                    total_frames=total_frames,
                    fps=self.fps,
                    x_original=self.x_original,
                    y_original=self.y_original,
                    z_original=self.z_original,
                    scatter=self.scatter,
                    ax=self.ax,
                    audio_features=self.audio_features
                )
                logger.debug(f"Effect instance created: {self.effect_name}, total_frames={total_frames}")
            except Exception as e:
                logger.error(f"Failed to create effect instance: {self.effect_name} - {e}", exc_info=True)
                self.effect_instance = None
    
    def update(self, current_time: float):
        """
        Update visualization for current playback time.
        
        Parameters:
            current_time: Current playback time in seconds
        """
        self.current_time = current_time
        
        if self.effect_instance is None:
            return
        
        # Convert playback time to frame number
        frame = int(current_time * self.fps)
        
        # Get total frames from effect
        total_frames = self.effect_instance.get_total_frames()
        
        # Clamp frame to valid range
        if frame >= total_frames:
            frame = total_frames - 1
        
        # Update effect
        try:
            result = self.effect_instance.update(frame)
            if result and len(result) > 0:
                self.scatter = result[0]
            
            # Update view limits based on current heart position
            if self.scatter and hasattr(self.scatter, '_offsets3d'):
                x_data, y_data, z_data = self.scatter._offsets3d
                if len(x_data) > 0:
                    margin = 2.0
                    self.ax.set_xlim([x_data.min() - margin, x_data.max() + margin])
                    self.ax.set_ylim([y_data.min() - margin, y_data.max() + margin])
                    self.ax.set_zlim([z_data.min() - margin, z_data.max() + margin])
            
            # Redraw canvas
            self.canvas.draw_idle()
        except Exception as e:
            logger.warning(f"Error updating visualization at frame {frame}: {e}", exc_info=True)
    
    def clear(self):
        """Clear visualization."""
        logger.debug("Clearing visualization")
        self.ax.clear()
        self.ax.set_facecolor('black')
        self.ax.grid(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.scatter = None
        self.effect_instance = None
        self.canvas.draw_idle()


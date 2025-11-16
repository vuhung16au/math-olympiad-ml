"""
Visualization Panel for MathHeart Player
Embedded matplotlib canvas for 3D heart visualization
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mathheart_player.player.heart_visualizer import HeartVisualizer

logger = logging.getLogger(__name__)


class VisualizationPanel(QWidget):
    """Panel for displaying 3D heart visualization."""
    
    def __init__(self, parent=None):
        """Initialize visualization panel."""
        super().__init__(parent)
        
        logger.info("Initializing VisualizationPanel")
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 6), facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        
        # Create heart visualizer
        logger.debug("Creating HeartVisualizer with default effect H8sync")
        self.visualizer = HeartVisualizer(self.canvas, effect_name='H8sync', density='lower')
        
        # Setup layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        logger.info("VisualizationPanel initialized")
    
    def set_effect(self, effect_name: str):
        """
        Set visualization effect.
        
        Parameters:
            effect_name: Effect name (H8sync, H9, H10)
        """
        logger.info(f"Setting visualization effect: {effect_name}")
        try:
            self.visualizer.set_effect(effect_name)
            logger.debug(f"Effect {effect_name} set successfully")
        except Exception as e:
            logger.warning(f"Failed to set effect {effect_name}: {e}", exc_info=True)
    
    def load_audio_features(self, audio_analyzer):
        """
        Load audio features for visualization.
        
        Parameters:
            audio_analyzer: AudioAnalyzer instance
        """
        logger.debug("Loading audio features into visualizer")
        try:
            self.visualizer.load_audio_features(audio_analyzer)
            logger.debug("Audio features loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load audio features: {e}", exc_info=True)
    
    def update_visualization(self, current_time: float):
        """
        Update visualization for current playback time.
        
        Parameters:
            current_time: Current playback time in seconds
        """
        self.visualizer.update(current_time)
    
    def clear(self):
        """Clear visualization."""
        self.visualizer.clear()


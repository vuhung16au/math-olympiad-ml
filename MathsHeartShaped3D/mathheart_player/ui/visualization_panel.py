"""
Visualization Panel for MathHeart Player
Embedded matplotlib canvas for 3D heart visualization
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mathheart_player.player.heart_visualizer import HeartVisualizer


class VisualizationPanel(QWidget):
    """Panel for displaying 3D heart visualization."""
    
    def __init__(self, parent=None):
        """Initialize visualization panel."""
        super().__init__(parent)
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(8, 6), facecolor='black')
        self.canvas = FigureCanvas(self.figure)
        
        # Create heart visualizer
        self.visualizer = HeartVisualizer(self.canvas, effect_name='H8sync', density='lower')
        
        # Setup layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def set_effect(self, effect_name: str):
        """
        Set visualization effect.
        
        Parameters:
            effect_name: Effect name (H8sync, H9, H10)
        """
        self.visualizer.set_effect(effect_name)
    
    def load_audio_features(self, audio_analyzer):
        """
        Load audio features for visualization.
        
        Parameters:
            audio_analyzer: AudioAnalyzer instance
        """
        self.visualizer.load_audio_features(audio_analyzer)
    
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


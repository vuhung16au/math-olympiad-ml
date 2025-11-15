"""
Effect registry and base class for heart animation effects.
"""

from abc import ABC, abstractmethod
import numpy as np

# Effect registry - will be populated by importing effect modules
_EFFECT_REGISTRY = {}


class BaseEffect(ABC):
    """
    Base class for all animation effects.
    
    Each effect must implement:
    - get_total_frames(): Return total number of frames
    - update(frame): Update animation for given frame, return (scatter,) tuple
    """
    
    def __init__(self, total_frames, fps, x_original, y_original, z_original, 
                 scatter, ax, audio_features=None):
        """
        Initialize effect with shared state.
        
        Parameters:
        - total_frames: Total number of frames for this effect
        - fps: Frames per second
        - x_original, y_original, z_original: Original heart coordinates
        - scatter: Matplotlib scatter plot object
        - ax: Matplotlib 3D axes object
        - audio_features: Optional dict with audio features for sync
        """
        self.total_frames = total_frames
        self.fps = fps
        self.x_original = x_original
        self.y_original = y_original
        self.z_original = z_original
        self.scatter = scatter
        self.ax = ax
        self.audio_features = audio_features or {}
    
    @abstractmethod
    def get_total_frames(self):
        """Return total frames for this effect."""
        pass
    
    @abstractmethod
    def update(self, frame):
        """
        Update animation for given frame.
        
        Parameters:
        - frame: Current frame number (0 to total_frames-1)
        
        Returns:
        - tuple: (scatter,) for matplotlib animation
        """
        pass
    
    def get_normalized_time(self, frame):
        """Get normalized time (0-1) for given frame."""
        return frame / self.total_frames
    
    def get_current_second(self, frame):
        """Get current time in seconds for given frame."""
        return frame / self.fps


def register_effect(effect_name, effect_class):
    """
    Register an effect class.
    
    Parameters:
    - effect_name: String identifier (e.g., 'A', 'B', 'H1')
    - effect_class: Effect class that inherits from BaseEffect
    """
    _EFFECT_REGISTRY[effect_name] = effect_class


def get_effect_class(effect_name):
    """
    Get effect class by name.
    
    Parameters:
    - effect_name: String identifier (e.g., 'A', 'B', 'H1')
    
    Returns:
    - Effect class or None if not found
    """
    return _EFFECT_REGISTRY.get(effect_name)


def get_all_effect_names():
    """Get list of all registered effect names."""
    return sorted(_EFFECT_REGISTRY.keys())


# Import all effects to register them
# This will populate the registry
try:
    from . import effect_a
    from . import effect_b
    from . import effect_c
    from . import effect_d
    from . import effect_e
    from . import effect_f
    from . import effect_g
    from . import effect_g1
    from . import effect_g2
    from . import effect_h1
    from . import effect_h2
    from . import effect_h3
    from . import effect_h4
    from . import effect_h5
    from . import effect_h6
    from . import effect_h7
    from . import effect_h8
    from . import effect_h8sync
    from . import effect_h8sync3min
except ImportError:
    # Effects not yet created, will be imported later
    pass

__all__ = ['BaseEffect', 'register_effect', 'get_effect_class', 'get_all_effect_names']


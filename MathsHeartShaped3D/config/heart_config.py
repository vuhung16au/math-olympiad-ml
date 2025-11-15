"""
Configurable heart formula parameters.

This module defines the parametric equations for the 3D heart shape.
The formula can be customized by modifying the HEART_FORMULA dictionary.
"""

# Default heart formula (original trio formula)
HEART_FORMULA = {
    'x_coeffs': [15, -4],  # [sin(v) coefficient, sin(3v) coefficient]
    'y_coeff': 8,          # cos(u) coefficient
    'z_coeffs': [15, -5, -2, -1],  # [cos(v), cos(2v), cos(3v), cos(v)] coefficients
    'y_flip': True  # If True, negate y to flip vertically (point down)
}

# Formula display strings for matplotlib
FORMULA_DISPLAY = {
    'x': r'$x = \sin(u) \cdot (15\sin(v) - 4\sin(3v))$',
    'y': r'$y = 8\cos(u)$',
    'z': r'$z = \sin(u) \cdot (15\cos(v) - 5\cos(2v) - 2\cos(3v) - \cos(v))$',
    'params': r'$u \in [0, \pi], \quad v \in [0, 2\pi]$'
}


def get_heart_formula():
    """
    Get the current heart formula configuration.
    
    Returns:
        dict: Heart formula parameters
    """
    return HEART_FORMULA.copy()


def get_formula_display():
    """
    Get LaTeX formula strings for display.
    
    Returns:
        dict: Formula display strings
    """
    return FORMULA_DISPLAY.copy()


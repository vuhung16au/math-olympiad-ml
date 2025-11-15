"""
Heart point generation with configurable formula.
"""

import numpy as np
from config.heart_config import get_heart_formula


def generate_heart_points(u_points=200, v_points=200, density='high', formula_config=None):
    """
    Generate 3D coordinates for the parametric heart shape.
    
    Parameters:
    - u_points: Number of points in the u parameter
    - v_points: Number of points in the v parameter
    - density: Point density level ('lower', 'low', 'medium', 'high')
    - formula_config: Optional dict to override default formula. If None, uses default.
    
    Returns:
    - x, y, z: Arrays of 3D coordinates
    - colors: Color values for the gradient
    """
    # Get formula configuration
    if formula_config is None:
        formula_config = get_heart_formula()
    
    # Adjust point count based on density
    density_multipliers = {
        'lower': 0.35,   # 70x70 = 4,900 points (~5,000)
        'low': 0.5,      # 100x100 = 10,000 points
        'medium': 0.75,  # 150x150 = 22,500 points
        'high': 1.0      # 200x200 = 40,000 points
    }
    multiplier = density_multipliers.get(density, 1.0)
    u_points = int(u_points * multiplier)
    v_points = int(v_points * multiplier)
    
    # Create parameter grids
    u = np.linspace(0, np.pi, u_points)
    v = np.linspace(0, 2 * np.pi, v_points)
    u_grid, v_grid = np.meshgrid(u, v)
    
    # Flatten for scatter plot
    u_flat = u_grid.flatten()
    v_flat = v_grid.flatten()
    
    # Extract formula coefficients
    x_coeffs = formula_config.get('x_coeffs', [15, -4])
    y_coeff = formula_config.get('y_coeff', 8)
    z_coeffs = formula_config.get('z_coeffs', [15, -5, -2, -1])
    y_flip = formula_config.get('y_flip', True)
    
    # Parametric equations for the 3D heart
    # x = sin(u) * (coeff1*sin(v) + coeff2*sin(3v))
    x = np.sin(u_flat) * (x_coeffs[0] * np.sin(v_flat) + x_coeffs[1] * np.sin(3 * v_flat))
    
    # y = coeff * cos(u) [with optional flip]
    y = y_coeff * np.cos(u_flat)
    if y_flip:
        y = -y  # Negative to flip vertically (point down)
    
    # z = sin(u) * (coeff1*cos(v) + coeff2*cos(2v) + coeff3*cos(3v) + coeff4*cos(v))
    z = np.sin(u_flat) * (
        z_coeffs[0] * np.cos(v_flat) +
        z_coeffs[1] * np.cos(2 * v_flat) +
        z_coeffs[2] * np.cos(3 * v_flat) +
        z_coeffs[3] * np.cos(v_flat)
    )
    
    # Use z values for color gradient
    colors = z
    
    return x, y, z, colors


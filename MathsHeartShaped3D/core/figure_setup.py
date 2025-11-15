"""
Matplotlib figure setup for 3D heart animation.
"""

import matplotlib.pyplot as plt
from config.heart_config import get_formula_display


def setup_figure(resolution='medium', dpi=100, show_axes=True, show_formulas=True, watermark='VUHUNG'):
    """
    Set up the matplotlib figure and 3D axes.
    
    Parameters:
    - resolution: 'small', 'medium', 'large', or '4k'
    - dpi: Dots per inch for the figure
    - show_axes: Whether to show coordinate axes
    - show_formulas: Whether to show parametric formulas
    - watermark: Watermark text to display (empty string for no watermark)
    
    Returns:
    - fig, ax: Matplotlib figure and axes objects
    """
    # Define resolution settings
    resolutions = {
        'small': (640, 480),
        'medium': (1280, 720),
        'large': (1920, 1080),
        '4k': (3840, 2160)
    }
    
    width, height = resolutions.get(resolution, resolutions['medium'])
    figsize = (width / dpi, height / dpi)
    
    # Create figure with black background
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Set initial view angle
    ax.view_init(elev=20, azim=45)
    
    # Force equal aspect ratio for 3D plot to fill screen properly
    ax.set_box_aspect([1, 1, 1])
    
    # Hide axes, grid, and panes
    ax.axis('off')
    ax.grid(False)
    
    # Make panes transparent/black
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('none')
    ax.yaxis.pane.set_edgecolor('none')
    ax.zaxis.pane.set_edgecolor('none')
    
    # Add coordinate axes if requested
    if show_axes:
        max_range = 20
        # X-axis (red)
        ax.plot([-max_range, max_range], [0, 0], [0, 0], 'r-', linewidth=1.5, alpha=0.6)
        # Y-axis (green)
        ax.plot([0, 0], [-max_range, max_range], [0, 0], 'g-', linewidth=1.5, alpha=0.6)
        # Z-axis (blue)
        ax.plot([0, 0], [0, 0], [-max_range, max_range], 'b-', linewidth=1.5, alpha=0.6)
    
    # Add formulas text if requested
    if show_formulas:
        formula_display = get_formula_display()
        formula_text = (
            formula_display['x'] + '\n' +
            formula_display['y'] + '\n' +
            formula_display['z'] + '\n' +
            formula_display['params']
        )
        fig.text(0.02, 0.98, formula_text, 
                transform=fig.transFigure,
                fontsize=10,
                verticalalignment='top',
                horizontalalignment='left',
                color='white',
                bbox=dict(boxstyle='round', facecolor='black', alpha=0.7, edgecolor='white', linewidth=0.5))
    
    # Add watermark if provided
    if watermark:
        # Very dark color (close to black background) - nearly invisible but visible
        # Using a very dark gray (#050505) that's slightly lighter than pure black
        # with low alpha to make it subtle and non-intrusive
        fig.text(0.5, 0.5, watermark,
                transform=fig.transFigure,
                fontsize=14,  # Medium size
                verticalalignment='center',
                horizontalalignment='center',
                color='#050505',  # Very dark gray, nearly invisible
                alpha=0.25,  # Low transparency for subtlety - nearly invisible but visible
                weight='normal')
    
    return fig, ax


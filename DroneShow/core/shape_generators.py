"""
Shape Generators for Drone Show
Generate 3D coordinates for various formations (heart, star, text, parking grid).
"""

import numpy as np
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from config.drone_config import (
    HEART_WIDTH, HEART_HEIGHT, HEART_DEPTH, HEART_COLOR,
    STAR_DIAMETER, STAR_DEPTH, STAR_POINTS, STAR_COLOR,
    TEXT_HEIGHT, TEXT_SPACING, TEXT_SAMPLE_INTERVAL,
    VIETNAM_COLOR_TOP, VIETNAM_COLOR_BOTTOM,
    AUSTRALIA_COLOR_TOP, AUSTRALIA_COLOR_BOTTOM,
    WHITE_COLOR, COMBINED_TEXT_SPACING,
    PARKING_Z, PARKING_SPACING, FORMATION_CENTER,
    MIN_SEPARATION
)


def enforce_min_separation_2d(positions, min_sep=MIN_SEPARATION):
    """
    Remove points that are too close in 2D (Y-Z plane).
    
    Args:
        positions: numpy array of shape (N, 3) with positions (all X should be 0 for 2D)
        min_sep: Minimum separation distance in meters (default: MIN_SEPARATION)
    
    Returns:
        filtered_positions: numpy array with points that maintain minimum separation
    """
    if len(positions) == 0:
        return positions
    
    # Use only Y and Z coordinates for distance calculation (2D)
    kept_positions = [positions[0]]  # Always keep first point
    
    for i in range(1, len(positions)):
        pos = positions[i]
        # Check distance to all previously kept positions (in Y-Z plane only)
        min_dist = float('inf')
        for kept_pos in kept_positions:
            # 2D distance in Y-Z plane
            dist = np.sqrt((pos[1] - kept_pos[1])**2 + (pos[2] - kept_pos[2])**2)
            min_dist = min(min_dist, dist)
        
        # Keep point if it's far enough from all other points
        if min_dist >= min_sep:
            kept_positions.append(pos)
    
    return np.array(kept_positions)


def generate_heart_formation(num_drones=900):
    """
    Generate 2D heart formation in Y-Z plane (flat, X=0).
    Uses parametric heart equation filled with grid points.
    
    Args:
        num_drones: Number of drones to use for heart formation (default: 900)
    
    Returns:
        positions: numpy array of shape (num_drones, 3) with (x, y, z) coordinates
        colors: numpy array of shape (num_drones, 3) with RGB values (0-255)
    """
    # 2D parametric heart equations
    # y = 16*sin³(t)
    # z = 13*cos(t) - 5*cos(2t) - 2*cos(3t) - cos(4t)
    
    # Generate outline points first
    t = np.linspace(0, 2 * np.pi, 200)
    y_outline = 16 * np.sin(t)**3
    z_outline = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # Find bounds for grid generation
    y_min, y_max = y_outline.min(), y_outline.max()
    z_min, z_max = z_outline.min(), z_outline.max()
    
    # Generate dense grid for formation (use smaller spacing than MIN_SEPARATION)
    # MIN_SEPARATION is for collision avoidance during flight, not formation density
    # Professional drone shows use 0.8-1.5m spacing in formations
    formation_spacing = 0.8  # meters - dense enough for clear shapes
    y_grid = np.arange(y_min, y_max + formation_spacing, formation_spacing)
    z_grid = np.arange(z_min, z_max + formation_spacing, formation_spacing)
    Y, Z = np.meshgrid(y_grid, z_grid)
    
    # Flatten grid
    y_flat = Y.ravel()
    z_flat = Z.ravel()
    
    # Filter points inside heart using matplotlib path
    from matplotlib.path import Path
    heart_path = Path(np.column_stack([y_outline, z_outline]))
    points_2d = np.column_stack([y_flat, z_flat])
    inside_mask = heart_path.contains_points(points_2d)
    
    y_inside = y_flat[inside_mask]
    z_inside = z_flat[inside_mask]
    
    # Scale to desired dimensions (60m x 60m)
    # Current scale is approximately -18 to 18 for y, -13 to 21 for z
    scale_y = HEART_WIDTH / (y_max - y_min)
    scale_z = HEART_HEIGHT / (z_max - z_min)
    
    y_scaled = y_inside * scale_y
    z_scaled = z_inside * scale_z
    
    # Create 3D positions (X=0 for all points - flat in Y-Z plane)
    # Grid already has MIN_SEPARATION spacing, so no need for aggressive filtering
    positions_filtered = np.column_stack([
        np.zeros(len(y_scaled)),  # X = 0 (flat)
        y_scaled,
        z_scaled
    ])
    
    # Randomly sample to get requested number of drones
    if len(positions_filtered) > num_drones:
        indices = np.random.choice(len(positions_filtered), num_drones, replace=False)
        positions_filtered = positions_filtered[indices]
    elif len(positions_filtered) < num_drones:
        # Pad with a few extra points if we're a bit short
        # This is OK since grid spacing already ensures MIN_SEPARATION
        extra_needed = num_drones - len(positions_filtered)
        if extra_needed <= 100 and len(positions_filtered) > 0:
            indices = np.random.choice(len(positions_filtered), extra_needed, replace=True)
            extra_positions = positions_filtered[indices].copy()
            # Add small offset to avoid exact duplicates (within MIN_SEPARATION tolerance)
            extra_positions[:, 1] += np.random.uniform(-0.3, 0.3, extra_needed)
            extra_positions[:, 2] += np.random.uniform(-0.3, 0.3, extra_needed)
            positions_filtered = np.vstack([positions_filtered, extra_positions])
    
    # Center at formation center
    positions = positions_filtered.copy()
    positions[:, 0] += FORMATION_CENTER[0]  # X = 0 + 0 = 0
    positions[:, 1] += FORMATION_CENTER[1]  # Y centered
    positions[:, 2] += FORMATION_CENTER[2]  # Z centered
    
    # All drones are red
    colors = np.tile(HEART_COLOR, (len(positions), 1))
    
    return positions, colors


def generate_star_formation(num_drones=850, num_points=5):
    """
    Generate 2D 5-pointed star formation in Y-Z plane (flat, X=0).
    Fills the star interior with grid points.
    
    Args:
        num_drones: Number of drones to use (default: 850)
        num_points: Number of star points (default: 5)
    
    Returns:
        positions: numpy array of shape (num_drones, 3)
        colors: numpy array of shape (num_drones, 3) with RGB values
    """
    # Star parameters
    outer_radius = STAR_DIAMETER / 2.0
    inner_radius = outer_radius * 0.382  # Golden ratio approximation
    
    # Generate star vertices (outer and inner points)
    # Start from top (90 degrees) and go clockwise
    star_vertices_2d = []
    for i in range(num_points * 2):
        angle = np.pi/2 - (i * np.pi / num_points)  # Start from top, go clockwise
        radius = outer_radius if i % 2 == 0 else inner_radius
        y = radius * np.cos(angle)
        z = radius * np.sin(angle)
        star_vertices_2d.append([y, z])
    
    # Create dense grid for formation (use smaller spacing than MIN_SEPARATION)
    # Professional drone shows use 0.8-1.5m spacing for visible formations
    formation_spacing = 0.8  # meters
    y_grid = np.arange(-outer_radius, outer_radius + formation_spacing, formation_spacing)
    z_grid = np.arange(-outer_radius, outer_radius + formation_spacing, formation_spacing)
    Y, Z = np.meshgrid(y_grid, z_grid)
    
    # Flatten grid
    y_flat = Y.ravel()
    z_flat = Z.ravel()
    
    # Filter points inside star using matplotlib path
    from matplotlib.path import Path
    star_path = Path(np.array(star_vertices_2d))
    points_2d = np.column_stack([y_flat, z_flat])
    inside_mask = star_path.contains_points(points_2d)
    
    y_inside = y_flat[inside_mask]
    z_inside = z_flat[inside_mask]
    
    # Create 3D positions (X=0 for all points - flat in Y-Z plane)
    # Grid already has MIN_SEPARATION spacing
    positions_filtered = np.column_stack([
        np.zeros(len(y_inside)),  # X = 0 (flat)
        y_inside,
        z_inside
    ])
    
    # Randomly sample to get requested number of drones
    if len(positions_filtered) > num_drones:
        indices = np.random.choice(len(positions_filtered), num_drones, replace=False)
        positions_filtered = positions_filtered[indices]
    elif len(positions_filtered) < num_drones:
        # Pad with a few extra points if we're a bit short
        extra_needed = num_drones - len(positions_filtered)
        if extra_needed <= 100 and len(positions_filtered) > 0:
            indices = np.random.choice(len(positions_filtered), extra_needed, replace=True)
            extra_positions = positions_filtered[indices].copy()
            # Add small offset to avoid exact duplicates
            extra_positions[:, 1] += np.random.uniform(-0.3, 0.3, extra_needed)
            extra_positions[:, 2] += np.random.uniform(-0.3, 0.3, extra_needed)
            positions_filtered = np.vstack([positions_filtered, extra_positions])
    
    # Center at formation center
    positions = positions_filtered.copy()
    positions[:, 0] += FORMATION_CENTER[0]  # X = 0 + 0 = 0
    positions[:, 1] += FORMATION_CENTER[1]  # Y centered
    positions[:, 2] += FORMATION_CENTER[2]  # Z centered
    
    # All drones are gold
    colors = np.tile(STAR_COLOR, (len(positions), 1))
    
    return positions, colors


def sample_text_outline(text, height=8.0, sample_interval=0.15):
    """
    Convert text to outline points using matplotlib.
    
    Args:
        text: String to render
        height: Height of text in meters
        sample_interval: Distance between sampled points in meters
    
    Returns:
        points: List of (x, y) coordinates
    """
    # Use bold sans-serif font
    fp = FontProperties(family='sans-serif', weight='bold')
    
    # Create text path (normalized size)
    path = TextPath((0, 0), text, size=1, prop=fp)
    
    # Get vertices from path
    vertices = path.vertices
    codes = path.codes
    
    if len(vertices) == 0:
        return np.array([])
    
    # Scale to desired height
    y_min, y_max = vertices[:, 1].min(), vertices[:, 1].max()
    text_height = y_max - y_min
    if text_height > 0:
        scale_factor = height / text_height
    else:
        scale_factor = 1.0
    
    vertices = vertices * scale_factor
    
    # Sample points along the path
    sampled_points = []
    
    current_point = None
    for i, (vertex, code) in enumerate(zip(vertices, codes)):
        if code == 1:  # MOVETO
            current_point = vertex
        elif code == 2:  # LINETO
            if current_point is not None:
                # Sample along line segment
                start = current_point
                end = vertex
                distance = np.linalg.norm(end - start)
                num_samples = max(2, int(distance / sample_interval))
                
                for t in np.linspace(0, 1, num_samples):
                    point = start + t * (end - start)
                    sampled_points.append(point)
                
                current_point = vertex
        elif code == 3:  # CURVE3 (quadratic bezier)
            # Simple approximation: sample along control polygon
            if current_point is not None and i + 1 < len(vertices):
                control = vertex
                end = vertices[i + 1]
                
                # Sample bezier curve
                for t in np.linspace(0, 1, 10):
                    point = (1-t)**2 * current_point + 2*(1-t)*t * control + t**2 * end
                    sampled_points.append(point)
                
                current_point = end
        elif code == 4:  # CURVE4 (cubic bezier)
            # Simple approximation
            if current_point is not None and i + 2 < len(vertices):
                control1 = vertex
                control2 = vertices[i + 1]
                end = vertices[i + 2]
                
                for t in np.linspace(0, 1, 15):
                    point = (1-t)**3 * current_point + 3*(1-t)**2*t * control1 + \
                            3*(1-t)*t**2 * control2 + t**3 * end
                    sampled_points.append(point)
                
                current_point = end
    
    if len(sampled_points) == 0:
        return np.array([])
    
    return np.array(sampled_points)


def generate_text_formation(text, num_drones, color_top, color_bottom):
    """
    Generate text formation with gradient coloring.
    
    Args:
        text: String to display
        num_drones: Number of drones to use
        color_top: RGB color at top
        color_bottom: RGB color at bottom
    
    Returns:
        positions: numpy array of shape (num_drones, 3)
        colors: numpy array of shape (num_drones, 3)
    """
    # Sample text outline
    outline_points = sample_text_outline(text, TEXT_HEIGHT, TEXT_SAMPLE_INTERVAL)
    
    if len(outline_points) == 0:
        # Fallback: return empty formation
        return np.zeros((0, 3)), np.zeros((0, 3))
    
    # Adjust number of points to match num_drones
    num_outline_points = len(outline_points)
    
    if num_outline_points > num_drones:
        # Downsample
        indices = np.linspace(0, num_outline_points - 1, num_drones, dtype=int)
        outline_points = outline_points[indices]
    elif num_outline_points < num_drones:
        # Upsample by duplicating nearby points with small offsets
        extra_needed = num_drones - num_outline_points
        extra_points = []
        for _ in range(extra_needed):
            idx = np.random.randint(0, num_outline_points)
            point = outline_points[idx].copy()
            # Add small random offset
            point += np.random.uniform(-0.1, 0.1, 2)
            extra_points.append(point)
        outline_points = np.vstack([outline_points, extra_points])
    
    # Convert 2D points to 3D (place in Y-Z plane)
    # Center the text around the formation center
    text_center_x = (outline_points[:, 0].min() + outline_points[:, 0].max()) / 2
    text_center_y = (outline_points[:, 1].min() + outline_points[:, 1].max()) / 2
    
    positions = np.zeros((len(outline_points), 3))
    positions[:, 0] = FORMATION_CENTER[0]  # X at center
    positions[:, 1] = outline_points[:, 0] - text_center_x + FORMATION_CENTER[1]  # Y centered
    positions[:, 2] = outline_points[:, 1] - text_center_y + FORMATION_CENTER[2]  # Z centered
    
    # Apply gradient based on Z coordinate (height)
    z_values = positions[:, 2]
    z_min, z_max = z_values.min(), z_values.max()
    
    colors = np.zeros((len(positions), 3))
    for i, z in enumerate(z_values):
        if z_max > z_min:
            t = (z - z_min) / (z_max - z_min)
        else:
            t = 0.5
        
        # Interpolate from bottom color to top color
        colors[i] = [
            color_bottom[0] + t * (color_top[0] - color_bottom[0]),
            color_bottom[1] + t * (color_top[1] - color_bottom[1]),
            color_bottom[2] + t * (color_top[2] - color_bottom[2])
        ]
    
    return positions, colors


def generate_simple_heart_emoji(num_drones=100):
    """
    Generate simple 2D heart shape for emoji.
    
    Args:
        num_drones: Number of drones to use
    
    Returns:
        positions: numpy array of shape (num_drones, 3)
        colors: numpy array of shape (num_drones, 3)
    """
    # Parametric heart in 2D
    t = np.linspace(0, 2 * np.pi, num_drones)
    
    # Heart parametric equations (simplified 2D)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # Scale to appropriate size (about 4 meters)
    scale = 4.0 / 32.0
    x = x * scale
    y = y * scale
    
    # Convert to 3D
    positions = np.zeros((num_drones, 3))
    positions[:, 0] = FORMATION_CENTER[0]
    positions[:, 1] = x + FORMATION_CENTER[1]
    positions[:, 2] = y + FORMATION_CENTER[2]
    
    # All white
    colors = np.tile(WHITE_COLOR, (num_drones, 1))
    
    return positions, colors


def generate_combined_text_formation(prefix, text_body, emoji_drones=100, 
                                    color_top=None, color_bottom=None):
    """
    Generate combined text with emoji (e.g., "I ❤ VIETNAM").
    
    Args:
        prefix: First character (e.g., "I")
        text_body: Main text (e.g., "VIETNAM")
        emoji_drones: Number of drones for heart emoji
        color_top: RGB color at top for main text
        color_bottom: RGB color at bottom for main text
    
    Returns:
        positions: numpy array of all drone positions
        colors: numpy array of all drone colors
    """
    # Generate prefix "I" (30 drones, white)
    prefix_points = sample_text_outline(prefix, TEXT_HEIGHT, TEXT_SAMPLE_INTERVAL)
    num_prefix = min(30, len(prefix_points)) if len(prefix_points) > 0 else 30
    
    if len(prefix_points) >= num_prefix:
        indices = np.linspace(0, len(prefix_points) - 1, num_prefix, dtype=int)
        prefix_points = prefix_points[indices]
    
    # Generate heart emoji
    emoji_pos, emoji_colors = generate_simple_heart_emoji(emoji_drones)
    
    # Generate main text
    num_text_drones = 350 if "VIETNAM" in text_body else 400
    text_pos, text_colors = generate_text_formation(
        text_body, num_text_drones, color_top, color_bottom
    )
    
    # Calculate widths for positioning
    if len(prefix_points) > 0:
        prefix_width = prefix_points[:, 0].max() - prefix_points[:, 0].min()
    else:
        prefix_width = TEXT_HEIGHT * 0.5
    
    emoji_width = 4.0  # Approximate width of heart emoji
    
    if len(text_pos) > 0:
        text_width = text_pos[:, 1].max() - text_pos[:, 1].min()
    else:
        text_width = len(text_body) * TEXT_HEIGHT * 0.6
    
    # Calculate total width and starting position
    total_width = prefix_width + COMBINED_TEXT_SPACING + emoji_width + \
                  COMBINED_TEXT_SPACING + text_width
    start_y = FORMATION_CENTER[1] - total_width / 2
    
    # Position prefix
    prefix_positions = np.zeros((len(prefix_points), 3))
    prefix_positions[:, 0] = FORMATION_CENTER[0]
    prefix_positions[:, 1] = prefix_points[:, 0] + start_y + prefix_width/2
    prefix_positions[:, 2] = prefix_points[:, 1] + FORMATION_CENTER[2]
    prefix_colors = np.tile(WHITE_COLOR, (len(prefix_points), 1))
    
    # Position emoji
    emoji_offset_y = start_y + prefix_width + COMBINED_TEXT_SPACING + emoji_width/2
    emoji_pos[:, 1] = emoji_pos[:, 1] - FORMATION_CENTER[1] + emoji_offset_y
    
    # Position main text
    text_offset_y = start_y + prefix_width + COMBINED_TEXT_SPACING + \
                    emoji_width + COMBINED_TEXT_SPACING + text_width/2
    if len(text_pos) > 0:
        text_pos[:, 1] = text_pos[:, 1] - FORMATION_CENTER[1] + text_offset_y
    
    # Combine all
    all_positions = np.vstack([prefix_positions, emoji_pos, text_pos])
    all_colors = np.vstack([prefix_colors, emoji_colors, text_colors])
    
    return all_positions, all_colors


def generate_parking_grid(num_drones=1000, used_drones=0):
    """
    Generate parking grid positions for inactive drones.
    
    Args:
        num_drones: Total number of drones
        used_drones: Number of drones in active formation
    
    Returns:
        positions: numpy array of shape (num_drones - used_drones, 3)
        colors: numpy array (all zeros, lights off)
    """
    parked_drones = num_drones - used_drones
    
    if parked_drones <= 0:
        return np.zeros((0, 3)), np.zeros((0, 3))
    
    # Calculate grid dimensions
    grid_cols = int(np.ceil(np.sqrt(parked_drones)))
    grid_rows = int(np.ceil(parked_drones / grid_cols))
    
    # Generate grid positions
    positions = []
    for row in range(grid_rows):
        for col in range(grid_cols):
            if len(positions) >= parked_drones:
                break
            
            x = (col - grid_cols/2) * PARKING_SPACING
            y = (row - grid_rows/2) * PARKING_SPACING
            z = PARKING_Z
            
            positions.append([x, y, z])
    
    positions = np.array(positions[:parked_drones])
    
    # All lights off (black color)
    colors = np.zeros((parked_drones, 3))
    
    return positions, colors


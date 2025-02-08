import numpy as np


def generate_circle_points(center=(0, 0), radius=10, num_points=50):
    """
    Generate (x, y) coordinates approximating a circle via a parametric
    equation.
    Return an Nx2 NumPy array of the circle's outline.
    """
    cx, cy = center
    t = np.linspace(0, 2 * np.pi, num_points)
    x = cx + radius * np.cos(t)
    y = cy + radius * np.sin(t)
    return np.column_stack((x, y))


def generate_square_points(center=(0, 0), side_length=20):
    """
    Generate (x, y) coordinates for a square (axis-aligned) centered at
    'center'.
    Returns an Nx2 array. Here N=5 so that the last point closes the polygon.
    """
    cx, cy = center
    half = side_length / 2.0
    # (x, y) corners in clockwise or counter-clockwise order, with last =
    # first to close polygon
    points = np.array([
        [cx - half, cy - half],
        [cx + half, cy - half],
        [cx + half, cy + half],
        [cx - half, cy + half],
        [cx - half, cy - half]  # repeat first corner to close
    ])
    return points

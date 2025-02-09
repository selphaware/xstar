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


def generate_isosceles_triangle_points(center=(0, 0), base=30, height=40):
    """
    Generate (x, y) coordinates for an isosceles triangle centered at 'center'.
    'base' is the width of the bottom side, 'height' is the vertical distance
    from the base to the apex.

    Returns an Nx2 array. The last point is the same as the first.
    """
    cx, cy = center
    half_base = base / 2.0

    # Let's place the triangle so that the base is at the bottom
    # and the apex is above.
    p1 = (cx - half_base, cy)  # bottom-left
    p2 = (cx + half_base, cy)  # bottom-right
    p3 = (cx, cy + height)  # apex

    points = np.array([p1, p2, p3, p1])  # repeat p1 to close
    return points


def generate_trapezium_points(center=(0, 0), top_width=20, bottom_width=40,
                              height=20):
    """
    Generate (x, y) coordinates for a simple trapezium (trapezoid) centered
    at 'center'.
    'top_width' is the length of the top side, 'bottom_width' is the length
    of the bottom side,
    'height' is the vertical distance from top to bottom.

    Returns an Nx2 array, with the last point = first point to close the shape.
    """
    cx, cy = center
    half_top = top_width / 2.0
    half_bottom = bottom_width / 2.0
    half_height = height / 2.0

    # We'll place the trapezium so that the center is the midpoint between
    # top and bottom,
    # with the top edge above the center and the bottom edge below the center.
    p1 = (cx - half_bottom, cy - half_height)  # bottom-left
    p2 = (cx + half_bottom, cy - half_height)  # bottom-right
    p3 = (cx + half_top, cy + half_height)  # top-right
    p4 = (cx - half_top, cy + half_height)  # top-left

    points = np.array([p1, p2, p3, p4, p1])
    return points


def generate_polygon_points(center=(0, 0), radius=20, num_sides=6):
    """
    Generate (x, y) coordinates for a regular polygon with 'num_sides',
    circumscribed by a circle of given 'radius', and centered at 'center'.

    Returns an Nx2 array with last point = first point to close the polygon.
    """
    cx, cy = center
    angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
    x_vals = cx + radius * np.cos(angles)
    y_vals = cy + radius * np.sin(angles)

    # Stack them and then repeat the first point
    points = np.column_stack((x_vals, y_vals))
    points = np.vstack([points, points[0]])  # close the polygon
    return points


def generate_spiked_circle_points(center=(0, 0), radius=20, num_spikes=8,
                                  spike_height=10):
    """
    Generate (x, y) coordinates for a spiked 'circle' shape:
    - 'num_spikes' is how many triangular spikes around the circle.
    - 'radius' is the main circle's radius.
    - 'spike_height' is how far each spike extends radially from the circle.

    The shape alternates between circle edge points and spike apex points.
    Returns an Nx2 array with the final point repeating the first to close.
    """
    cx, cy = center
    # We have 2*num_spikes points around the circle (excluding the closing
    # point),
    # because each spike has a 'base point' on the circle and an 'apex'
    # outward.
    # For N spikes, we basically double the resolution.
    base_angles = np.linspace(0, 2 * np.pi, num_spikes, endpoint=False)

    points_list = []
    for angle in base_angles:
        # 1) Circle edge point
        x_circle = cx + radius * np.cos(angle)
        y_circle = cy + radius * np.sin(angle)
        points_list.append((x_circle, y_circle))

        # 2) Spike apex point
        x_spike = cx + (radius + spike_height) * np.cos(angle)
        y_spike = cy + (radius + spike_height) * np.sin(angle)
        points_list.append((x_spike, y_spike))

    # Convert to array and repeat the first point
    points = np.array(points_list)
    points = np.vstack([points, points[0]])
    return points

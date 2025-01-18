import numpy as np

from xmath.pcurve import (
    generate_parametric_values,
    generate_parametric_bool_grid
)
from xmath.plotfuncs import plot_boolean_grid, plot_parametric
from xmath.structures import R2


def test_log_spiral():
    # Example usage
    _C = 1
    _L = .075
    _t_range = (0, 40)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)

    coordinates = generate_parametric_values(
        "log_spiral",
        list(t_values),
        _C, _L
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_circle():
    # Example usage
    _R = 10
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "circle",
        list(t_values),
        _R
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_asteroid_curve():
    # Example usage
    _C = 10
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "asteroid_curve",
        list(t_values),
        _C
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_epitrochoid_curve():
    # Example usage
    _c: float = .5  # between 0 - 1
    _n: int = 15
    _t_range = (0, 1000)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates: R2 = generate_parametric_values(
        "epitrochoid",
        list(t_values),
        _c, _n
    )

    # apply factor
    factor: float = 100.
    coordinates: R2 = [
        (x * factor, y * factor)
        for (x, y) in coordinates
    ]

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_lemniscate_bernoulli_curve():
    # Example usage
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "lemniscate_bernoulli",
        list(t_values),
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_log_spiral_circle():
    _C = 0.1
    _L = 0.1
    _R = 750
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)

    spiral = generate_parametric_values(
        "log_spiral",
        list(t_values),
        _C, _L
    )

    circle = generate_parametric_values(
        "circle",
        list(t_values),
        _R
    )

    plot_parametric([spiral, circle])


if __name__ == "__main__":
    # test_log_spiral()
    # test_circle()
    # test_asteroid_curve()
    # test_log_spiral_circle()
    test_epitrochoid_curve()

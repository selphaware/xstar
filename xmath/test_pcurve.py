from typing import Tuple, List
from xmath.pcurve import (
    generate_parametric_values,
    generate_parametric_bool_grid,
    generate_multi_param_bool_grid
)
from xmath.plotfuncs import plot_boolean_grid, plot_parametric
from xmath.structures import R2


def _gen_bool_and_plot(coordinates: R2):
    bool_grid = generate_parametric_bool_grid(coordinates)

    shape: Tuple[int, int] = (len(bool_grid[0]), len(bool_grid))
    print("Shape: ", shape)

    origin = (shape[0] // 2 - 1, shape[1] // 2)
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def _gen_multi_bool_and_plot(mcoordinates: List[R2]):
    bool_grid = generate_multi_param_bool_grid(mcoordinates)

    shape: Tuple[int, int] = (len(bool_grid[0]), len(bool_grid))
    print("Shape: ", shape)

    origin = (shape[0] // 2 - 1, shape[1] // 2)
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric(mcoordinates)


def test_multi_circle():
    _R = 8
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 25

    mcoords = [

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            _R / x, 0, 0
        )
        for x
        # in [2 ** y for y in range(15)]
        in range(1, 16)
    ]

    _gen_multi_bool_and_plot(mcoords)


def test_log_spiral():
    # Example usage
    _C = 1
    _L = .075
    _t_range = (0, 40)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        _C, _L, 0, 0
    )

    _gen_bool_and_plot(coordinates)


def test_log_spiral_shift():
    # Example usage
    _C = 1
    _L = .075
    _t_range = (0, 40)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        _C, _L, 10, 10
    )

    _gen_bool_and_plot(coordinates)


def test_circle():
    # Example usage
    _R = 10
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "circle",
        _t_range,
        _num_points,
        _factor,
        _R, 0, 0
    )

    _gen_bool_and_plot(coordinates)


def test_circle_shift():
    # Example usage
    _R = 10
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "circle",
        _t_range,
        _num_points,
        _factor,
        _R, -10, -10
    )

    _gen_bool_and_plot(coordinates)


def test_asteroid_curve():
    # Example usage
    _C = 10
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "asteroid_curve",
        _t_range,
        _num_points,
        _factor,
        _C
    )

    _gen_bool_and_plot(coordinates)


def test_epitrochoid_curve():
    # Example usage
    _c: float = .5  # between 0 - 1
    _n: int = 15
    _t_range = (0, 1000)
    _num_points = 1000
    _factor: float = 100.

    coordinates: R2 = generate_parametric_values(
        "epitrochoid",
        _t_range, _num_points, _factor,
        _c, _n
    )

    _gen_bool_and_plot(coordinates)


def test_lemniscate_bernoulli_curve():
    # Example usage
    _t_range = (0, 350)
    _num_points = 1000
    _factor = 15

    coordinates = generate_parametric_values(
        "lemniscate_bernoulli",
        _t_range,
        _num_points,
        _factor
    )

    _gen_bool_and_plot(coordinates)


def test_log_spiral_circle():
    _C = 10.
    _L = -.1
    _R = 4
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 10

    mcoords = [

        # 2 log spirals i.e. 2 blackholes

        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor,
            _C, _L, 0, 0
        ),

        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor,
            _C, _L, -1, -1
        ),

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            _R, 0, 0
        ),

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            _R, 1, 1
        )
    ]

    _gen_multi_bool_and_plot(mcoords)


if __name__ == "__main__":
    # test_log_spiral()
    # test_circle()
    # test_circle_shift()
    # test_log_spiral_shift()
    # test_asteroid_curve()
    # test_epitrochoid_curve()
    # test_lemniscate_bernoulli_curve()

    # combination
    test_log_spiral_circle()
    test_multi_circle()

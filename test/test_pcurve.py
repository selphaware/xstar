from typing import Tuple, List

from xmath.pcurve import (
    generate_parametric_values,
    generate_parametric_num_grid,
    generate_multi_param_num_grid
)
from xmath.plotfuncs import plot_num_grid, plot_parametric
from xmath.structures import R2
from xmath.xrandom import random_int_generator


def _gen_bool_and_plot(coordinates: R2):
    bool_grid = generate_parametric_num_grid(coordinates)

    shape: Tuple[int, int] = (len(bool_grid[0]), len(bool_grid))
    print("Shape: ", shape)

    origin = (
        int(round(shape[0] / 2, 0)) - 1,
        int(round(shape[1] / 2, 0)) - 1
    )
    print("Origin: ", origin)

    bool_grid[origin[0]][origin[1]] = len(coordinates)

    plot_num_grid(bool_grid)

    plot_parametric([coordinates])


def _gen_multi_bool_and_plot(mcoordinates: List[R2]):
    bool_grid = generate_multi_param_num_grid(mcoordinates)

    shape: Tuple[int, int] = (len(bool_grid[0]), len(bool_grid))
    print("Shape: ", shape)

    origin = (
        int(round(shape[0] / 2, 0)) - 1,
        int(round(shape[1] / 2, 0)) - 1
    )
    print("Origin: ", origin)

    bool_grid[origin[0]][origin[1]] = len(mcoordinates)

    plot_num_grid(bool_grid)

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
            r=_R / x, hs=0, vs=0
        )
        for x
        # in [2 ** y for y in range(15)]
        in range(1, 16)
    ]

    _gen_multi_bool_and_plot(mcoords)


def test_multi_circle_elipse():
    _R = 18
    _a = 20
    _b = 16
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 25

    mcoords = [

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R - x, hs=0, vs=0
            # r=_R / x, hs=0, vs=0
        )
        for x
        # in [2 ** y for y in range(15)]
        in range(1, 16)
        if x % 2 == 1
    ]

    mcoords.extend([

        generate_parametric_values(
            "elipse",
            _t_range,
            _num_points,
            _factor,
            a=_a - x, b=_b - x, hs=0, vs=0
            # a=_a / x, b=_b / x, hs=0, vs=0
        )
        for x
        # in [2 ** y for y in range(15)]
        in range(1, 16)
        if x % 2 == 0
    ])

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
        C=_C, L=_L, hs=0, vs=0
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
        C=_C, L=_L, hs=15, vs=15
    )

    _gen_bool_and_plot(coordinates)


def test_big_log_spirals():
    # Example usage
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = (10 ** -32) / 5
    print(_factor)

    rnd = random_int_generator(1, 30, unique=True)

    coordinates = [generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        C=_C, L=_L, hs=0, vs=0
    )]

    coordinates.extend([
        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor + (_i * _factor / 10),
            C=_C, L=_L, hs=next(rnd) / _factor, vs=next(rnd) / _factor
        )
        for _i in range(15)
    ])

    for coordinate in coordinates:
        print(max([x for (x, y) in coordinate]))
        print(max([y for (x, y) in coordinate]))

    plot_parametric(coordinates)
    # _gen_bool_and_plot(coordinates)


def test_multi_big_log_spirals():
    # Example usage
    _C = 1
    _L = .075
    _t_range = (0, 1_000)
    _num_points = 100_000
    _factor = 1

    universe_coordinates = [
        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor + (_i / 10),
            C=_C, L=_L, hs=0, vs=0
        )
        for _i in range(10)
    ]

    _C = 1
    _L = .075
    _t_range = (0, 1_0)
    _num_points = 1_000
    _factor = 1

    universe_galaxy_coordinates = [
        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor + (_i / 10),
            C=_C, L=_L, hs=o1, vs=o2
        )
        for coord_set in universe_coordinates
        for _j, (o1, o2) in enumerate(coord_set)
        for _i in range(10)
        if (o1 + o1 >= 4) and (_j % 1000 == 0)
    ]

    plot_parametric(universe_galaxy_coordinates)
    # _gen_bool_and_plot(coordinates)


def test_elipse():
    # Example usage
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "elipse",
        _t_range,
        _num_points,
        _factor,
        a=5, b=30, hs=0, vs=0
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
        r=_R, hs=0, vs=0
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
        r=_R, hs=10, vs=10
    )

    _gen_bool_and_plot(coordinates)


def test_circle_shift2():
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
        r=_R, hs=5, vs=10
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
        C=_C
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
        c=_c, n=_n
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
            C=_C, L=_L, hs=0, vs=0
        ),

        generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor,
            C=_C, L=_L, hs=-1, vs=-1
        ),

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R, hs=0, vs=0
        ),

        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R, hs=1, vs=1
        )
    ]

    _gen_multi_bool_and_plot(mcoords)


if __name__ == "__main__":
    # test_elipse()
    # test_log_spiral()
    # test_circle()
    # test_circle_shift()
    # test_circle_shift2()
    # test_log_spiral_shift()
    # test_asteroid_curve()
    # test_epitrochoid_curve()
    # test_lemniscate_bernoulli_curve()

    # combination
    # test_log_spiral_circle()
    # test_multi_circle()
    # test_multi_circle_elipse()
    test_big_log_spirals()
    # test_multi_big_log_spirals()
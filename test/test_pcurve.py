from bisect import bisect
from typing import Tuple, List
from math import pi
import numpy as np
from pprint import pp

from space.cosmic_structures.functions.calculate import calculate_magnitude, \
    get_vector_between_positions
from space.universe import Universe
from xmath.generate_universe import generate_universe_parametric_values
from xmath.pcurve import (
    generate_parametric_values,
    generate_parametric_num_grid,
    generate_multi_param_num_grid
)
from xmath.plotfuncs import plot_num_grid, plot_parametric, \
    plot_parametric_universe
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


def test_log_spiral2():
    # Example usage
    _a_C = 1
    _b_C = 2
    _L = .075
    _t_range = (0, 40)
    _num_points = 1000
    _factor = 1

    coordinates = generate_parametric_values(
        "log_spiral2",
        _t_range,
        _num_points,
        _factor,
        a_C=_a_C, b_C=_b_C, L=_L, rot=2 * pi, hs=0, vs=0
    )

    print(coordinates)

    plot_parametric("LSR Test", [coordinates], show=True)

def test_log_spiral_shift():
    # Example usage
    _C = 1
    _L = .015
    _t_range = (0, 250)
    _num_points = 2000
    _factor = 1

    coordinates = generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        C=_C, L=_L, hs=15, vs=15
    )

    plot_parametric([coordinates])


def test_big_log_spirals():
    # Example usage
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = (10 ** -32) / 5
    print(_factor)

    num_galaxies = 10
    rnd = random_int_generator(-num_galaxies, num_galaxies, unique=True)

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
        for _i in range(num_galaxies)
    ])

    for coordinate in coordinates:
        print(max([x for (x, y) in coordinate]))
        print(max([y for (x, y) in coordinate]))

    plot_parametric(coordinates)
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


def test_log_spiral3():
    # Example usage
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = (10 ** -32) / 5

    coordinates = generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        C=_C, L=_L, hs=0, vs=0
    )

    c3 = coordinates[0: 9500]
    c4 = coordinates[9500:]

    rnd_int3 = random_int_generator(0, len(c3) - 1, True)
    rnd_int4 = random_int_generator(0, len(c4) - 1, True)

    _R = 0.01
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    planets = [
        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R / x, hs=o1, vs=o2
        )
        for (o1, o2) in [(0, 0)] + [c4[next(rnd_int4)] for _ in range(200)]
        for x in range(1, 16)
    ]

    galaxy = [coordinates] + planets

    plot_parametric(galaxy)


def test_log_spiral4():
    galaxy1 = generate_galaxy((0, 0), 100)
    galaxy2 = generate_galaxy((1, 1), 100)

    plot_parametric(galaxy1 + galaxy2)


def test_log_spiral5():
    universe = []
    for j in range(0, 60, 10):
        for i in range(0, 60, 10):
            universe.extend(generate_galaxy((i, j), 20))

    plot_parametric(universe)


def test_log_spiral6():
    universe = []
    i_rand = random_int_generator(0, 60)
    j_rand = random_int_generator(0, 60)
    _ = next(i_rand)
    for j in range(0, 60, 10):
        for i in range(0, 60, 10):
            universe.extend(generate_galaxy(
                (next(i_rand), next(j_rand)),
                20
            ))

    print(universe)

    plot_parametric(universe)


def test_log_spiral7():
    universe = []
    i_rand = random_int_generator(0, 60)
    j_rand = random_int_generator(0, 60)
    _ = next(i_rand)
    for j in range(0, 60, 10):
        for i in range(0, 60, 10):
            universe.extend(generate_galaxy2(
                (next(i_rand), next(j_rand)),
                20
            ))

    print(universe)

    plot_parametric(universe)


def generate_galaxy(
        origin: Tuple[int, int],
        num_systems: int
):
    # Example usage
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = (10 ** -32) / 5

    coordinates = generate_parametric_values(
        "log_spiral",
        _t_range,
        _num_points,
        _factor,
        C=_C, L=_L, hs=origin[0], vs=origin[1]
    )

    magnitudes = np.array([
        calculate_magnitude(
            get_vector_between_positions(origin, x),
            roundit=False
        )
        for x in coordinates
    ])
    min_mag, max_mag = min(magnitudes), max(magnitudes)
    print(f"min={min_mag}, max={max_mag}")
    even_space = np.linspace(min_mag, max_mag, num_systems)
    locations = [
        coordinates[bisect(list(magnitudes), x) - 1]
        for x in even_space
    ]

    # rnd_int3 = random_int_generator(0, len(c3) - 1, True)
    # rnd_int4 = random_int_generator(0, len(c4) - 1, True)

    _R = 0.01
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1
    _ofactor = (10 ** -32) / 5

    planets = [
        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R / x,
            hs=o1,
            vs=o2
        )
        for (o1, o2) in locations
        for x in range(1, 16)
    ]

    galaxy = [coordinates] + planets

    return galaxy


def generate_galaxy2(
        origin: Tuple[int, int],
        num_systems: int
):
    # Example usage
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = (10 ** -32) / 5

    coordinates = []
    for x in range(5):
        coordinates.append(generate_parametric_values(
            "log_spiral",
            _t_range,
            _num_points,
            _factor * x,
            C=_C, L=_L, hs=origin[0], vs=origin[1]
        ))

    coordinates = np.concatenate(coordinates)

    # unique values
    vv = []
    new_cc = []
    for cc in coordinates:
        if cc not in vv:
            new_cc.append(cc)

    coordinates = np.array(new_cc)

    magnitudes = np.array([
        calculate_magnitude(
            get_vector_between_positions(origin, x),
            roundit=False
        )
        for x in coordinates
    ])
    min_mag, max_mag = min(magnitudes), max(magnitudes)
    print(f"min={min_mag}, max={max_mag}")
    even_space = np.linspace(min_mag, max_mag, num_systems)
    locations = [
        coordinates[bisect(list(magnitudes), x) - 1]
        for x in even_space
    ]

    # rnd_int3 = random_int_generator(0, len(c3) - 1, True)
    # rnd_int4 = random_int_generator(0, len(c4) - 1, True)

    _R = 0.01
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1
    _ofactor = (10 ** -32) / 5

    planets = [
        generate_parametric_values(
            "circle",
            _t_range,
            _num_points,
            _factor,
            r=_R / x,
            hs=o1,
            vs=o2
        )
        for (o1, o2) in locations
        for x in range(1, 16)
    ]

    galaxy = [coordinates] + planets

    return galaxy


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

    # test_big_log_spirals()

    # test_log_spiral2()
    # test_log_spiral4()
    # test_log_spiral5()
    # test_log_spiral6()
    # test_log_spiral7()

    # test_multi_big_log_spirals()

    _aq = Universe(
        10,
        75,
        16,
        30,
        10,
        20
    )

    print(_aq.universe_positions)

    plot_parametric_universe(
        _aq.universe_positions,
        show_galaxy_motion_path=True,
        show_planets_motion_path=True,
        show_stars=True,
        show_black_holes=True,
        show_planets=True
    )

    import pdb
    pdb.set_trace()

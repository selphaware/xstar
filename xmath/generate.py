from bisect import bisect
import numpy as np
from typing import Tuple

from space.cosmic_structures.functions.calculate import calculate_magnitude, \
    get_vector_between_positions
from xmath.pcurve import generate_parametric_values
from xmath.xrandom import random_int_generator


def generate_galaxy_parametric_values(
        # galaxy
        origin: Tuple[int, int],
        galaxy_density: int = 5,

        # planetary systems
        num_systems: int = 20,
        num_planet_orbits: int = 16
):
    # rand factor
    rnd_factor = random_int_generator(1, 10)

    # galaxy parametric parameters
    _C = 1
    _L = 0.075
    _t_range = (0, 1_000)
    _num_points = 10_000
    _factor = ((10 ** -32) / 5) * (next(rnd_factor) / 2)

    coordinates = []
    for x in range(galaxy_density):
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
        for x in range(1, num_planet_orbits + 1)
    ]

    galaxy = [coordinates] + planets

    return galaxy

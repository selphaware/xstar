from bisect import bisect
from typing import Tuple, List
import random
import numpy as np

from space.cosmic_structures.functions.calculate import \
    get_distance_between_positions, calculate_magnitude, \
    get_vector_between_positions
from xmath.pcurve import generate_parametric_values
from xmath.plotfuncs import plot_parametric_universe
from xmath.structures import UNIVERSE_STRUCT, R2, Z2, Z2_POS
from xmath.xrandom import random_int_generator


def generate_universe_parametric_values(
        num_galaxies: int = 36,
        num_systems: int = 20,
        num_planet_orbits: int = 16
) -> UNIVERSE_STRUCT:
    rand_size_range: Tuple[int, int] = (0, int(num_galaxies * 5))
    universe = {}

    visited = []
    for galaxy in range(num_galaxies):

        galaxy_size, origin = calculate_galaxy_origin(rand_size_range, visited)

        visited.append(origin)
        universe[f"Galaxy {galaxy}"] = generate_galaxy_parametric_values(
            f"Galaxy {galaxy}",
            (float(origin[0]), float(origin[1])),
            galaxy_size,
            num_systems,
            num_planet_orbits
        )

    return universe


# TODO: Simplify this
def calculate_galaxy_origin(rand_size_range: Z2_POS, visited: List[Z2_POS]):
    i_rand = random_int_generator(*rand_size_range, seed="I_RAND")
    j_rand = random_int_generator(*rand_size_range, seed="J_RAND")
    rnd_factor = random_int_generator(5, 20, seed="FACTOR")

    origin = None
    galaxy_size = next(rnd_factor) / 10
    while True:
        origin = (next(i_rand), next(j_rand))

        too_close = [
            get_distance_between_positions(origin, _x)
            for _x in visited
        ]

        too_close = [_x for _x in too_close if _x < 10]

        if len(too_close) == 0:
            break
    return galaxy_size, origin


def generate_galaxy_parametric_values(
        galaxy_name: str,
        origin: Tuple[float, float] = (0, 0),
        galaxy_size: int = 1,
        num_systems: int = 20,
        num_planet_orbits: int = 16,
):
    # galaxy parametric parameters
    _C = 1
    _L = 0.015
    _t_range = (0, 250)
    _num_points = 2_000
    _factor = .1 * galaxy_size

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
    locations.insert(0,
                     (float(origin[0]), float(origin[1])))

    # rnd_int3 = random_int_generator(0, len(c3) - 1, True)
    # rnd_int4 = random_int_generator(0, len(c4) - 1, True)

    _R = 0.01
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1

    evenly_spaced_orbit = lambda _radius, _r_factor: _radius - (
        _radius * (_r_factor / (num_planet_orbits + 1))
    )

    star_systems = {
        f"{galaxy_name}, System {system_no}":
        {
            "name": f"{galaxy_name}, System {system_no}",

            "origin": [[(o1, o2)]],

            "is_centre": (o1, o2) == origin,

            "planet_orbit_path": ( planet_orbit_paths := [
                generate_parametric_values(
                    "circle",
                    _t_range,
                    _num_points,
                    _factor,
                    r=evenly_spaced_orbit(_R, x),
                    hs=o1,
                    vs=o2
                )
                for x in range(1, num_planet_orbits + 1)
            ] ),

            "planets": [
                [random.choice(planet_coords)]
                for planet_coords in planet_orbit_paths
            ]
        }
        for system_no, (o1, o2) in enumerate(locations)
    }

    galaxy = {
        "name": galaxy_name,
        "motion_path": coordinates,
        "star_systems": star_systems
    }

    return galaxy

import datetime
import time
from bisect import bisect
from typing import Tuple, List
import random
import numpy as np
from math import pi

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
        num_planet_orbits: int = 16,
        rand_size_range_limit: int = 5,
        galaxy_distance: float = 10.,
        black_hole_distance: float = 3.,
        num_black_holes: int = 10
) -> UNIVERSE_STRUCT:
    rand_size_range: Tuple[int, int] = (
        0, rand_size_range_limit
    )
    universe = {}

    visited = []
    for galaxy in range(num_galaxies):

        rnd_systems = random_int_generator(
            num_systems - int(.25 * num_systems),
            num_systems + int(.25 * num_systems),
            "SYSTEMS-X1"
        )

        galaxy_size, origin = calculate_origin(
            rand_size_range,
            visited,
            galaxy_distance
        )

        visited.append(origin)
        universe[f"Galaxy {galaxy}"] = generate_galaxy_parametric_values(
            f"Galaxy {galaxy}",
            (float(origin[0]), float(origin[1])),
            galaxy_size,
            next(rnd_systems),
            num_planet_orbits
        )

    # Add other universe stellar objects
    rnd_stellar = random_int_generator(0, 10, "STELLAR")
    for _ibx in range(num_black_holes):
        _, origin = calculate_origin(
            rand_size_range,
            visited,
            black_hole_distance
        )
        universe[f"Black Hole BH{_ibx}"] = generate_galaxy_parametric_values(
            f"Black Hole BH{_ibx}",
            (float(origin[0]), float(origin[1])),
            next(rnd_stellar) / 10,
            0,
            0
        )

    return universe


# TODO: Simplify this
def calculate_origin(
        rand_size_range: Z2_POS,
        visited: List[Z2_POS],
        distance: float = 10.
):
    i_rand = random_int_generator(*rand_size_range, seed="I_RAND")
    j_rand = random_int_generator(*rand_size_range, seed="J_RAND")
    rnd_factor = random_int_generator(5, 20, seed="FACTOR")

    origin = None
    galaxy_size = next(rnd_factor) / 10
    for _ in range(rand_size_range[1] ** 2):
        origin = (next(i_rand), next(j_rand))

        too_close = [
            get_distance_between_positions(origin, _x)
            for _x in visited
        ]

        too_close = [_x for _x in too_close if _x < distance]

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
    elip_rnd_a = random_int_generator(10, 15, "AELIP_LOG_A")
    elip_rnd_b = random_int_generator(10, 15, "BELIP_LOG_B")

    _a_C = next(elip_rnd_a) / 10.
    _b_C = next(elip_rnd_b) / 10.
    _L = 0.015
    _t_range = (0, 250)
    _num_points = 2_000
    _factor = .1 * galaxy_size

    coordinates = generate_parametric_values(
        "log_spiral_elipse",
        _t_range,
        _num_points,
        _factor,
        hs=origin[0], vs=origin[1],

        # log spiral params
        a_C=_a_C, b_C=_b_C,
        rot=random.choice([2 * pi * x / 20. for x in range(0, 20)]),
        L=_L
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

    star_locs = [
        coordinates[bisect(list(magnitudes), x) - 1]
        for x in even_space
    ]
    star_locs.insert(0,
                     (float(origin[0]), float(origin[1])))

    star_systems = generate_star_systems_parametric_values(
        galaxy_name, num_planet_orbits, origin, star_locs
    )

    galaxy = {
        "name": galaxy_name,
        "motion_path": coordinates,
        "star_systems": star_systems
    }

    return galaxy


def generate_star_systems_parametric_values(galaxy_name, num_planet_orbits,
                                            origin, star_locs):
    _R = 0.01
    _t_range = (0, 100)
    _num_points = 1000
    _factor = 1
    rnd_planets = random_int_generator(
        num_planet_orbits - int(.75 * num_planet_orbits),
        num_planet_orbits + int(.5 * num_planet_orbits),
        "RND_PLANETS-Y2"
    )
    evenly_spaced_orbit = lambda _radius, _r_factor, _rrrn: _radius - (
            _radius * (_r_factor / (_rrrn + 1))
    )
    star_systems = {
        f"System {system_no}":
            {
                "name": (sys_name := f"{galaxy_name}: System {system_no}"),
                "origin": [(o1, o2)],
                "is_centre": (is_centre := (o1, o2) == origin),
                "star_name": f"Black Hole: {sys_name}" \
                    if is_centre else f"Star: {sys_name}",
                "num_planets": (_rn := next(rnd_planets)),
                "planet_orbit_paths": (planet_orbit_paths := [
                    generate_parametric_values(
                        "circle",
                        _t_range,
                        _num_points,
                        _factor,
                        r=evenly_spaced_orbit(_R, x, _rn),
                        hs=o1,
                        vs=o2
                    )
                    for x in range(1, _rn + 1)
                ]),
                "planets": generate_planets_parametric_values(
                    planet_orbit_paths, sys_name
                )
            }
        for system_no, (o1, o2) in enumerate(star_locs)
    }
    return star_systems


def generate_planets_parametric_values(planet_orbit_paths, sys_name):
    return {
        f"Planet {_idxp}": {
            "name": f"{sys_name}: Planet {_idxp}",
            "position": [random.choice(planet_coords)],
            "motion_path": planet_coords
        }
        for _idxp, planet_coords in enumerate(planet_orbit_paths)
    }

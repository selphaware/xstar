from typing import List, Tuple, Union

from xmath.pcurve import (
    generate_multi_param_num_grid,
    calculate_offset_positions, generate_parametric_values
)
from xmath.structures import R2, Z2_MATRIX, Z2, Z2_POS, R2_POS


def calculate_int_positions(
        real_positions: List[R2]
) -> Tuple[Z2_MATRIX, List[Z2], Z2_POS, Z2_POS]:
    position_grid: Z2_MATRIX = generate_multi_param_num_grid(
        real_positions
    )

    position_coords: List[Z2] = [
        calculate_offset_positions(planet_position_array)[0]
        for planet_position_array in real_positions
    ]

    shape: Z2_POS = (len(position_grid[0]),
                     len(position_grid))

    origin: Z2_POS = (
        int(round(shape[0] / 2, 0)) - 1,
        int(round(shape[1] / 2, 0)) - 1
    )

    return position_grid, position_coords, shape, origin


def calculate_real_positions(
        num_planets: int,
        evenly_spaced: bool = False
) -> List[R2]:
    time_range = (0, 100)
    num_points = 1000
    factor = 25
    planet_range = range(1, num_planets + 1)
    dist_metric = lambda rator, denom: rator - denom \
        if evenly_spaced else rator / denom

    planet_real_positions = [
        generate_parametric_values(
            "circle",
            time_range,
            num_points,
            factor,
            r=dist_metric(18, x), hs=0, vs=0
        )
        for x in planet_range
        if x % 2 == 1
    ]

    planet_real_positions.extend([
        generate_parametric_values(
            "elipse",
            time_range,
            num_points,
            factor,
            a=dist_metric(20, x), b=dist_metric(16, x),
            hs=0, vs=0
        )
        for x in planet_range
        if x % 2 == 0
    ])

    return planet_real_positions


def get_vector_between_positions(
        x1: Union[Z2_POS, R2_POS],
        x2: Union[Z2_POS, R2_POS]
) -> Z2_POS:
    return (x2[0] - x1[0], x2[1] - x1[0])


def get_distance_between_positions(
        x1: Union[Z2_POS, R2_POS],
        x2: Union[Z2_POS, R2_POS],
        roundit: bool = True
) -> Union[float, int]:
    a, b = get_vector_between_positions(x1, x2)
    dist = ((a ** 2) + (b ** 2)) ** .5
    dist = int(round(dist, 0)) if roundit else dist

    return dist

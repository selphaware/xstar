from typing import List, Dict, Any, Tuple

import numpy as np

from structures import (
    Lambda,
    R1, R2, R2_POS, Z2_POS,
    Z2,
    Z2_MATRIX
)
from xmath.equations import PARAMETRIC_EQNS


# TODO: Refactor to compute x and y values directly
#  passing through the series/array rather than
#  calculate each value

def generate_parametric_values(
        equation_type: str,
        t_range: Z2_POS,
        num_points: int,
        factor: float,
        *parameter_values
) -> R2:
    t_values: R1 = list(np.linspace(t_range[0], t_range[1], num_points))

    equation: List[Lambda] = PARAMETRIC_EQNS[equation_type]
    eqn_x: Lambda = equation[0]
    eqn_y: Lambda = equation[1]

    results: R2 = []
    for i, t in enumerate(t_values):
        x: float = eqn_x(t, *parameter_values)
        y: float = eqn_y(t, *parameter_values)
        val: R2_POS = (x, y)
        results.append(val)

    results: R2 = [
        (x * factor, y * factor)
        for (x, y) in results
    ]

    return results

# TODO: bool --> int
def generate_multi_param_object_grid(mvalues: List[R2]) -> Z2_MATRIX:
    cvalues: R2 = []

    markers: List[Tuple[int, int]] = [(0, 1)]

    for idx, values in enumerate(mvalues):
        cvalues.extend(values)
        markers.append((len(cvalues), idx + 2))

    bool_grid: Z2_MATRIX = generate_parametric_object_grid(cvalues, markers)

    return bool_grid


# TODO: bool -> int
def generate_parametric_object_grid(
        values: R2,
        markers: List[Tuple[int, int]]
) -> Z2_MATRIX:
    # rounded ints from floats
    rounded: Z2 = [
        (int(x), int(y))
        for (x, y) in values
    ]

    # calc. offset (grid has to be in +ve region)
    max_x: int = max([x[0] for x in rounded])
    max_y: int = max([y[1] for y in rounded])
    min_x: int = min([x[0] for x in rounded])
    min_y: int = min([y[1] for y in rounded])

    offset_x: int = -1 * min_x if min_x < 0 else min_x
    offset_y: int = -1 * min_y if min_y < 0 else min_y

    # adjust for offset
    new_vals: Z2 = [
        (x + offset_x, y + offset_y)
        for (x, y) in rounded
    ]

    # populate grid: True where there is a value, ow: False
    range_x: range = range(max_x + offset_x + 1)
    range_y: range = range(max_y + offset_y + 1)

    grid: Z2_MATRIX = [[0 for _ in range_x] for _ in range_y]
    for idx, new_val in enumerate(new_vals):
        x_index: int = new_val[0]
        y_index: int = new_val[1]

        marker = [y for (x, y) in markers if idx >= x][-1]

        grid[y_index][x_index] = marker

    return grid


def generate_bool_grid(
        t_range: Z2_POS,
        num_points: int,
        factor: float,
        **eqn_params: Dict[str, List[Any]]
) -> Z2_MATRIX:
    mcoords = [
        generate_parametric_values(
            equation, t_range, num_points, factor, parameters
        )
        for equation, parameters in eqn_params.items()
    ]

    bool_grid = generate_multi_param_object_grid(mcoords)

    return bool_grid

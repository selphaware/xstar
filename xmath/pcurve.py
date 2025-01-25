from typing import List, Tuple, Optional
from inspect import signature
import numpy as np

from xmath.structures import (
    Lambda,
    R1, R2, R2_POS, Z2_POS,
    Z2,
    Z2_MATRIX
)
from xmath.equations import PARAMETRIC_EQNS


# TODO: Refactor to OPTIMIZE:
#  compute x and y values directly
#  passing through the series/array
#  rather than calculate each value

def generate_parametric_values(
        equation_type: str,
        t_range: Z2_POS,
        num_points: int,
        factor: float,
        **parameter_values
) -> R2:
    t_values: R1 = list(np.linspace(t_range[0], t_range[1], num_points))

    equation: List[Lambda] = PARAMETRIC_EQNS[equation_type]
    eqn_x: Lambda = equation[0]
    eqn_y: Lambda = equation[1]
    sig_x: List[str] = list(signature(eqn_x).parameters.keys())
    sig_y: List[str] = list(signature(eqn_y).parameters.keys())

    results: R2 = []
    for i, t in enumerate(t_values):
        x: float = eqn_x(
            t,
            **{k: v for k, v in parameter_values.items() if k in sig_x}
        )

        y: float = eqn_y(
            t,
            **{k: v for k, v in parameter_values.items() if k in sig_y}
        )

        val: R2_POS = (x, y)
        results.append(val)

    results: R2 = [
        (x * factor, y * factor)
        for (x, y) in results
    ]

    return results


def generate_multi_param_num_grid(mvalues: List[R2]) -> Z2_MATRIX:
    cvalues: R2 = []

    markers: List[Tuple[int, int]] = [(0, 1)]

    for idx, values in enumerate(mvalues):
        cvalues.extend(values)
        markers.append((len(cvalues), idx + 2))

    bool_grid: Z2_MATRIX = generate_parametric_num_grid(cvalues, markers)

    return bool_grid


def generate_parametric_num_grid(
        values: R2,
        markers: Optional[List[Tuple[int, int]]] = None
) -> Z2_MATRIX:
    if markers is None:
        markers: List[Tuple[int, int]] = [(0, 1)]

    # int_vals ints from floats
    new_vals, range_x, range_y = calculate_offset_positions(values)

    grid: Z2_MATRIX = [[0 for _ in range_x] for _ in range_y]
    for idx, new_val in enumerate(new_vals):
        x_index: int = new_val[0]
        y_index: int = new_val[1]

        marker = [m2 for (m1, m2) in markers if idx >= m1][-1]

        grid[y_index][x_index] = marker

    return grid


def calculate_offset_positions(values: R2) -> Tuple[Z2, range, range]:
    int_vals: Z2 = [
        (
            int(round(x, 0)), int(round(y, 0))
        )
        for (x, y) in values
    ]
    # calc. offset (grid has to be in +ve region)
    max_x: int = max([x[0] for x in int_vals])
    max_y: int = max([y[1] for y in int_vals])
    min_x: int = min([x[0] for x in int_vals])
    min_y: int = min([y[1] for y in int_vals])
    offset_x: int = -1 * min_x if min_x < 0 else 0
    offset_y: int = -1 * min_y if min_y < 0 else 0
    # adjust for offset
    new_vals: Z2 = [
        (x + offset_x, y + offset_y)
        for (x, y) in int_vals
    ]
    # populate grid: True where there is a value, ow: False
    range_x: range = range(max_x + offset_x + 1)
    range_y: range = range(max_y + offset_y + 1)
    return new_vals, range_x, range_y

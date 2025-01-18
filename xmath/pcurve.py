from typing import List, Tuple

from structures import (
    Lambda,
    R1, R2, R2_POS, Z2_POS,
    Z2,
    BOOL2
)
from xmath.equations import PARAMETRIC_EQNS


def generate_parametric_values(
        equation_type: str,
        t_values: R1,
        *parameter_values
) -> R2:
    equation: List[Lambda] = PARAMETRIC_EQNS[equation_type]
    eqn_x: Lambda = equation[0]
    eqn_y: Lambda = equation[1]

    results: R2 = []
    for i, t in enumerate(t_values):
        x: float = eqn_x(t, *parameter_values)
        y: float = eqn_y(t, *parameter_values)
        val: R2_POS = (x, y)
        results.append(val)

    return results


def generate_parametric_bool_grid(values: R2) -> Tuple[BOOL2, Z2_POS]:
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

    origin: Z2_POS = (0, 0)
    grid: BOOL2 = [[False for _ in range_y] for _ in range_x]
    for idx, new_val in enumerate(new_vals):
        x_index: int = new_val[0]
        y_index: int = new_val[1]
        grid[x_index][y_index] = True

        if idx == 0:
            # used for:
            # galaxy: blackhole at the centre
            # system: star at the centre
            origin = (x_index, y_index)

    return grid, origin

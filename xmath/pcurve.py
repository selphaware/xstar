from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

from structures import (
    Lambda,
    R1, R2, R2_POS, Z2_POS,
    Z1, Z2,
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


def plot_parametric(values: List[R2]):
    # Extract x and y values for plotting
    x_values: List[R1] = []
    y_values: List[R1] = []
    for _values in values:
        x_values.append([coord[0] for coord in _values])
        y_values.append([coord[1] for coord in _values])

    # Plotting
    plt.figure(figsize=(8, 6))
    for i in range(len(values)):
        plt.plot(x_values[i], y_values[i], label=f"Curve {i}")

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Parametric Curve")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_boolean_grid(grid: BOOL2):
    # Convert the boolean grid to integers for better visualization
    int_grid: List[Z1] = [[1 if cell else 0 for cell in row] for row in grid]

    # Plot the grid
    plt.figure(figsize=(8, 8))
    plt.imshow(int_grid, cmap='Greys', origin='upper')
    plt.colorbar(label="Shaded (1) / Unshaded (0)")
    plt.title("Boolean Grid Visualization")
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")

    # Set x-axis ticks to match the number of columns
    plt.xticks(range(len(grid[0])))

    # Set y-axis ticks to match the number of rows
    plt.yticks(range(len(grid)))

    plt.grid(visible=False)
    plt.show()


def test_log_spiral():
    # Example usage
    _C = 1
    _L = .075
    _t_range = (0, 40)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)

    coordinates = generate_parametric_values(
        "log_spiral",
        list(t_values),
        _C, _L
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_circle():
    # Example usage
    _R = 10
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "circle",
        list(t_values),
        _R
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_asteroid_curve():
    # Example usage
    _C = 10
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "asteroid_curve",
        list(t_values),
        _C
    )

    bool_grid, origin = generate_parametric_bool_grid(coordinates)
    print(bool_grid)
    print("Shape: ", len(bool_grid), len(bool_grid[0]))
    print("Origin: ", origin)

    plot_boolean_grid(bool_grid)

    plot_parametric([coordinates])


def test_log_spiral_circle():
    _C = 0.1
    _L = 0.1
    _R = 750
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)

    spiral = generate_parametric_values(
        "log_spiral",
        list(t_values),
        _C, _L
    )

    circle = generate_parametric_values(
        "circle",
        list(t_values),
        _R
    )

    plot_parametric([spiral, circle])


if __name__ == "__main__":
    test_log_spiral()
    # test_circle()
    # test_asteroid_curve()
    # test_log_spiral_circle()

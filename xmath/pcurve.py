from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt

INT_R1 = List[int]
INT_R2 = List[INT_R1]

FLOAT_R1 = List[float]
FLOAT_R2 = List[FLOAT_R1]

BOOL_R1 = List[bool]
BOOL_R2 = List[BOOL_R1]

PARAMETRIC_EQNS = {

    "log_spiral": [
        lambda t, C, L: C * np.exp(L * t) * np.cos(t),
        lambda t, C, L: C * np.exp(L * t) * np.sin(t)
    ],

    "circle": [
        lambda t, r: r * np.cos(t),
        lambda t, r: r * np.sin(t)
    ],

    "asteroid_curve": [
        lambda t, C: C * (np.cos(t) ** 3),
        lambda t, C: C * (np.sin(t) ** 3)
    ]

}


def generate_parametric_values(
        equation_type: str,
        t_values: FLOAT_R1,
        *parameter_values
) -> FLOAT_R2:
    equation = PARAMETRIC_EQNS[equation_type]
    eqn_x = equation[0]
    eqn_y = equation[1]

    results = []
    for i, t in enumerate(t_values):
        x = eqn_x(t, *parameter_values)
        y = eqn_y(t, *parameter_values)
        results.append([x, y])

    return results


def generate_bool_grid(
        values_2d: FLOAT_R2
) -> Tuple[BOOL_R2, Tuple[int, int]]:
    rounded: INT_R2 = [
        [int(x), int(y)]
        for [x, y] in values_2d
    ]

    max_x = max([x[0] for x in rounded])
    max_y = max([y[1] for y in rounded])
    min_x = min([x[0] for x in rounded])
    min_y = min([y[1] for y in rounded])

    offset_x = -1 * min_x if min_x < 0 else min_x
    offset_y = -1 * min_y if min_y < 0 else min_y

    new_vals: INT_R2 = [
        [x + offset_x, y + offset_y]
        for [x, y] in rounded
    ]

    range_x = range(max_x + offset_x + 1)
    range_y = range(max_y + offset_y + 1)

    grid: BOOL_R2 = [[False for _ in range_y] for _ in range_x]
    origin = (0, 0)
    for idx, new_val in enumerate(new_vals):
        x_index = new_val[0]
        y_index = new_val[1]
        grid[x_index][y_index] = True

        if idx == 0:
            origin = (x_index, y_index)

    return grid, origin


def plot_parametric(values: List[FLOAT_R2]):
    # Extract x and y values for plotting
    x_values = []
    y_values = []
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


def plot_boolean_grid(grid: BOOL_R2):
    # Convert the boolean grid to integers for better visualization
    int_grid = [[1 if cell else 0 for cell in row] for row in grid]

    # Plot the grid
    plt.figure(figsize=(8, 8))
    plt.imshow(int_grid, cmap='Greys', origin='upper')
    plt.colorbar(label="Shaded (1) / Unshaded (0)")
    plt.title("Boolean Grid Visualization")
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")
    plt.xticks(
        range(len(grid[0])))  # Set x-axis ticks to match the number of columns
    plt.yticks(
        range(len(grid)))  # Set y-axis ticks to match the number of rows
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

    bool_grid, origin = generate_bool_grid(coordinates)
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

    bool_grid, origin = generate_bool_grid(coordinates)
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

    bool_grid, origin = generate_bool_grid(coordinates)
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
    # test_log_spiral_circle()
    test_circle()

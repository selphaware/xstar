from typing import List
import numpy as np
import matplotlib.pyplot as plt

FLOAT_R1 = List[float]
FLOAT_R2 = List[FLOAT_R1]

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
    for t in t_values:
        x = eqn_x(t, *parameter_values)
        y = eqn_y(t, *parameter_values)
        results.append([x, y])
    return results


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


def test_log_spiral():
    # Example usage
    _C = 0.1
    _L = 0.1
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "log_spiral",
        list(t_values),
        _C, _L
    )
    plot_parametric([coordinates])


def test_circle():
    # Example usage
    _R = 1
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "circle",
        list(t_values),
        _R
    )
    plot_parametric([coordinates])


def test_asteroid_curve():
    # Example usage
    _C = 1
    _t_range = (0, 100)
    _num_points = 1000

    t_values = np.linspace(_t_range[0], _t_range[1], _num_points)
    coordinates = generate_parametric_values(
        "asteroid_curve",
        list(t_values),
        _C
    )
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
    test_asteroid_curve()

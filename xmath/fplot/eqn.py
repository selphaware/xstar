from typing import Tuple
import numpy as np

# Dictionary of parametric curves
eqns = {
    "log_spiral_elipse": [
        lambda t, a_C, b_C, L, rot: a_C * np.exp(L * t) * np.cos(rot + t),
        lambda t, a_C, b_C, L, rot: b_C * np.exp(L * t) * np.sin(rot + t)
    ],

    "circle_elipse": [
        lambda t, a, b, rot: a * np.cos(rot + t),
        lambda t, a, b, rot: b * np.sin(rot + t)
    ],

    "rectangle": [
        lambda t, a, b, rot: a * np.cos(
            rot + t
        ) / np.maximum(
            np.abs(np.cos(t)),
            np.abs(np.sin(t))
        ),

        lambda t, a, b, rot: b * np.sin(
            rot + t
        ) / np.maximum(
            np.abs(np.cos(t)),
            np.abs(np.sin(t))
        )
    ]

}


def compute_values(
        curve_type: str,
        shift: float,
        t_min: float = 0.0,
        t_max: float = 10.0,
        num_points: int = 1000,
        **curve_params
) -> Tuple[np.array, np.array, np.array]:
    """

    :param shift:
    :param curve_type:
    :param t_min:
    :param t_max:
    :param num_points:
    :param curve_params:
    :return:
    """

    # Get the parametric functions x(t) and y(t)
    x_func, y_func = eqns[curve_type]

    # Create a linspace for t
    t_vals = np.linspace(t_min, t_max, num_points)

    # Evaluate x(t), y(t)
    x_vals = x_func(t_vals, **curve_params)
    y_vals = y_func(t_vals, **curve_params)

    return t_vals, x_vals + shift, y_vals + shift

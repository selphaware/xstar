from typing import Tuple, Dict
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from xmath.fplot.eqn import compute_values


def plot_static_values(
        curve_type: str,
        t_min: float = 0.,
        t_max: float = 10.,
        num_points: int = 1000,
        plot_type: str = "r-",
        xlim: Tuple[int, int] = (-20, 20),
        ylim: Tuple[int, int] = (-10, 10),
        **curve_params
):
    """

    :param curve_type:
    :param t_min:
    :param t_max:
    :param num_points:
    :param plot_type:
    :param curve_params:
    :return:
    """
    # Compute spiral data
    t_vals, x_vals, y_vals = compute_values(
        curve_type,
        0, 0,
        t_min=t_min,
        t_max=t_max,
        num_points=num_points,

        # params
        **curve_params
    )

    plt.rcParams.update({
        'axes.facecolor': 'black',  # Black background for all axes
        'axes.edgecolor': 'white',  # White border
        'axes.labelcolor': 'white',  # White axis labels
        'xtick.color': 'yellow',  # White tick marks
        'ytick.color': 'yellow',  # White tick marks
        'grid.color': 'dimgray',  # Dark grey grid lines
        'figure.facecolor': 'black',  # Black figure background
    })

    # Plot
    fig, ax = plt.subplots()
    plt.gca().set_aspect('equal')

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    ax.plot(x_vals, y_vals, plot_type)
    ax.grid(True)

    plt.title(curve_type)
    plt.xlabel("x1")
    plt.ylabel("x2")

    plt.tight_layout()

    plt.show()


def animate(
        curve_type: str,
        t_min: float = 0.0,
        t_max: float = 10.0,
        num_points: int = 1000,
        frames: int = 100,
        interval: int = 50,
        _xlim: Tuple[int, int] = (-20, 20),
        _ylim: Tuple[int, int] = (-10, 10),
        centre: bool = False,
        **master_params
):
    """

    :param curve_type:
    :param t_min:
    :param t_max:
    :param frames:
    :param interval:
    :param master_params:
    :return:
    """
    curve_params: Dict[str, float] = master_params.get("curve_params")
    curve_shift_params: Dict[str, float] = master_params.get(
        "curve_shift_params"
    )
    shift_params: Dict[str, float] = master_params.get("shift_params")
    point_params: Dict[str, float] = master_params.get("point_params")

    plt.rcParams.update({
        'axes.facecolor': 'black',  # Black background for all axes
        'axes.edgecolor': 'white',  # White border
        'axes.labelcolor': 'white',  # White axis labels
        'xtick.color': 'yellow',  # White tick marks
        'ytick.color': 'yellow',  # White tick marks
        'grid.color': 'dimgray',  # Dark grey grid lines
        'figure.facecolor': 'black',  # Black figure background
    })

    fig, ax = plt.subplots()
    plt.gca().set_aspect('equal')

    line, = ax.plot([], [], 'r-')
    point, = ax.plot([], [], "o")

    xlim = list(_xlim)
    ylim = list(_ylim)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(curve_type)

    # Optional: add a grid
    ax.grid(True)

    def init():
        # Initialize the line to empty
        line.set_data([], [])
        point.set_data([], [])
        return line, point

    def update(frame: int):
        updated_params = {
            k: v * frame + curve_params[k]
            for k, v in curve_shift_params.items()
        }

        _, x_vals, y_vals = compute_values(
            curve_type,
            shift_params['x'] * frame,
            shift_params['y'] * frame,
            t_min,
            t_max,
            num_points,
            **updated_params
        )

        if centre:
            xlim[0] += shift_params['x']
            xlim[1] += shift_params['x']
            ylim[0] += shift_params['y']
            ylim[1] += shift_params['y']

        else:
            veri_len = (_ylim[1] - _ylim[0])
            hori_len = (_xlim[1] - _xlim[0])

            if min(y_vals) <= ylim[0]:
                ylim[1] -= veri_len
                ylim[0] -= veri_len

            if max(y_vals) >= ylim[1]:
                ylim[1] += veri_len
                ylim[0] += veri_len

            if min(x_vals) <= xlim[0]:
                xlim[1] -= hori_len
                xlim[0] -= hori_len

            if max(x_vals) >= xlim[1]:
                xlim[1] += hori_len
                xlim[0] += hori_len

        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)

        # Update the line data
        # print(x_vals[-2:], y_vals[-2:])
        line.set_data(x_vals, y_vals)
        point.set_data([x_vals[-1]], [y_vals[-1]])

        return line, point

    # Create the animation
    anim = FuncAnimation(
        fig,
        update,  # function called for each frame
        frames=frames,  # how many frames total
        init_func=init,  # sets up background
        blit=False,  # improves performance
        interval=interval  # delay between frames in ms
    )

    plt.show()
    return anim


# Example usage
if __name__ == "__main__":
    base_inputs = [
        0,  # t_min
        100,  # t_max
        10000,  # num points
        10000,  # num frames
        25,  # intervals
        (-2000, 2000), (-1000, 1000),  # xlim, ylim
        True
    ]

    animate(
        "rectangle",
        *base_inputs,
        curve_params={"a": 5, "b": 2, "rot": 0},
        curve_shift_params={"a": 0, "b": 0, "rot": 0.0},
        shift_params={"x": 5.9, "y": 2.1}
    )

    animate(
        "log_spiral_elipse",
        *base_inputs,
        curve_params={"a": 1, "b": 1, "L": 0.055, "rot": 0},
        curve_shift_params={"a": 0, "b": 0, "L": 0, "rot": 0.1},
        shift_params={"x": 0.9, "y": -2.1}
    )

    animate(
        "circle_elipse",
        *base_inputs,
        curve_params={"a": 5, "b": 2, "rot": 0},
        curve_shift_params={"a": 0.1, "b": 0.1, "rot": 0.1},
        shift_params={"x": -10.9, "y": 0.1}
    )

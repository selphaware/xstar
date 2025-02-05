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
        xlim: Tuple[int, int] = (-20, 20),
        ylim: Tuple[int, int] = (-10, 10),
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

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_title(curve_type)

    # Optional: add a grid
    ax.grid(True)

    def init():
        # Initialize the line to empty
        line.set_data([], [])
        point.set_data([], [])
        return (line,)

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
        blit=True,  # improves performance
        interval=interval  # delay between frames in ms
    )

    plt.show()
    return anim


# Example usage
if __name__ == "__main__":
    plot_static = False
    if plot_static:
        plot_static_values(
            "circle_elipse",
            0,
            10,
            1000,
            a=1,
            b=1,
            rot=0
        )

    animate(
        "rectangle",
        0,
        100,
        10000,
        10000,
        25,
        (-200, 200), (-100, 100),
        curve_params={
            "a": 5,
            "b": 2,
            "rot": 0
        },
        curve_shift_params={
            "a": 0,
            "b": 0,
            "rot": 0.01
        },
        shift_params={
            "x": 0.1,
            "y": 0.1
        }
    )

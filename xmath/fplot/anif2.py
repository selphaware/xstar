from pprint import pp
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
        t_min: float = 0.0,
        t_max: float = 10.0,
        num_points: int = 1000,
        frames: int = 100,
        interval: int = 50,
        _xlim: Tuple[int, int] = (-20, 20),
        _ylim: Tuple[int, int] = (-10, 10),
        centre: bool = False,
        **master_object_params
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

    for masterk, masterv in master_object_params.items():
        master_object_params[masterk]["plot"], = ax.plot(
            [], [],
            master_object_params[masterk]["symbol"]
        )

    xlim = list(_xlim)
    ylim = list(_ylim)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)

    # Optional: add a grid
    ax.grid(True)

    def init():
        # Initialize the line to empty
        for masterk, masterv in master_object_params.items():
            master_object_params[masterk]["plot"].set_data([], [])

        return tuple([
            master_object_params[k]["plot"]
            for k, v in master_object_params.items()
        ])

    def update(frame: int):
        for obj, master_params in master_object_params.items():
            curve_params = master_params["curve_params"]
            curve_shift_params = master_params["curve_shift_params"]
            velocity_vector = master_params["velocity_vector"]
            origin = master_params["origin"]

            master_params["updated_params"] = {
                k: v * frame + curve_params[k]
                for k, v in curve_shift_params.items()
            }

            _, x_vals, y_vals = compute_values(
                master_params["curve_type"],
                velocity_vector['x'] * frame + origin[0],
                velocity_vector['y'] * frame + origin[1],
                t_min,
                t_max,
                num_points,
                **master_params["updated_params"]
            )

            master_params["x_vals"] = x_vals
            master_params["y_vals"] = y_vals

        velocity_vector = master_object_params["main"]["velocity_vector"]
        x_vals = master_object_params["main"]["x_vals"]
        y_vals = master_object_params["main"]["y_vals"]

        if centre:
            xlim[0] += velocity_vector['x']
            xlim[1] += velocity_vector['x']
            ylim[0] += velocity_vector['y']
            ylim[1] += velocity_vector['y']

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
        ret = []
        for masterk, masterv in master_object_params.items():
            if masterv["last"]:
                masterv["plot"].set_data(
                    [masterv["x_vals"][-1]], [masterv["y_vals"][-1]]
                )
            else:
                masterv["plot"].set_data(
                    masterv["x_vals"], masterv["y_vals"]
                )
            masterv["plot"].set_color(masterv["color"])
            ret.append(masterv["plot"])

        return tuple(ret)

    # Create the animation
    anim = FuncAnimation(
        fig,
        update,  # function called for each frame
        frames=frames,  # how many frames total
        init_func=init,  # sets up background
        blit=False,  # improves performance
        interval=interval  # delay between frames in ms
    )

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
    return anim


def test_moving_gun():
    base_inputs = [
        0,  # t_min
        100,  # t_max
        10000,  # num points
        10000,  # num frames
        25,  # intervals
        (-2000, 2000), (-1000, 1000),  # xlim, ylim
        True
    ]
    objects = {
        "main": {
            "curve_type": "rectangle",
            "origin": (0, 0),
            "symbol": "r-",
            "curve_params": {"a": 100, "b": 50, "rot": 0},
            "curve_shift_params": {"a": 0, "b": 0, "rot": 0},
            "velocity_vector": {"x": 3, "y": 1},
            "color": "cyan",
            "last": False
        },

        "gun": {
            "curve_type": "circle_elipse",
            "origin": (-100, -50),
            "symbol": "r-",
            "curve_params": {"a": 10, "b": 10, "rot": 0},
            "curve_shift_params": {"a": 0, "b": 0, "rot": 0},
            "velocity_vector": {"x": -7, "y": -7},
            "color": "yellow",
            "last": False,
        }
    }
    pp(base_inputs)
    pp(objects)
    animate(*base_inputs, **objects)


# Example usage
if __name__ == "__main__":
    test_moving_gun()

from typing import Tuple
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
        0,
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


def animate_spiral_rotation(curve_type="log_spiral_elipse",
                            a_C=1.0, b_C=1.0, L=0.1,
                            rot_step=0.01,
                            a_C_step=0.01,
                            b_C_step=0.01,
                            # how much to increment rotation each frame
                            frames=100,  # total frames
                            t_min=0.0, t_max=10.0,
                            interval=50):
    """
    Animate the spiral while incrementing 'rot' by 'rot_step' each frame.
    """
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'r-')  # a single line object we'll update
    point, = ax.plot([], [], "o")

    # Set plot bounds so we can see the curve (adjust as needed)
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_title("Rotating Log-Spiral Ellipse")

    # Optional: add a grid
    ax.grid(True)

    def init():
        # Initialize the line to empty
        line.set_data([], [])
        point.set_data([], [])
        return (line,)

    def update(frame):
        # Current rotation = frame index * rot_step
        current_rot = frame * rot_step

        # expand/contract horizontally and vertically
        frame_bin_size = 10E2
        frame_bin = frames // frame_bin_size
        current_a_C = a_C  # abs(np.cos(2 * pi * frame / frame_bin)) * a_C +
        # a_C
        current_b_C = b_C  # abs(np.sin(2 * pi * frame / frame_bin)) * b_C +
        # b_C

        # Compute x,y for that rotation
        _, x_vals, y_vals = compute_values(
            curve_type,
            frame / 10,
            a=current_a_C,
            b=current_b_C,
            # L=L,
            rot=0,  # current_rot,  # rotation changes each frame
            t_min=t_min,
            t_max=t_max
        )
        # Update the line data
        # print(x_vals[-2:], y_vals[-2:])
        line.set_data(x_vals, y_vals)
        point.set_data([x_vals[-1]], [y_vals[-1]])
        return (line, point)

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
    plot_static_values(
        "circle_elipse",
        0,
        10,
        1000,
        a=1,
        b=1,
        rot=0
    )

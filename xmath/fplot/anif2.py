from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Dictionary of parametric curves
curves = {
    "log_spiral_elipse": [
        lambda t, a_C, b_C, L, rot: a_C * np.exp(L * t) * np.cos(rot + t),
        lambda t, a_C, b_C, L, rot: b_C * np.exp(L * t) * np.sin(rot + t)
    ],

    "circle_elipse": [
        lambda t, a, b, rot: a * np.cos(rot + t),
        lambda t, a, b, rot: b * np.sin(rot + t)
    ],

    "square": [
        lambda t, a, b, rot: a * np.cos(
            rot + t
        ) / np.maximum(
            np.abs(np.cos(rot + t)),
            np.abs(np.sin(rot + t))
        ),

        lambda t, a, b, rot: b * np.sin(
            rot + t
        ) / np.maximum(
            np.abs(np.cos(rot + t)),
            np.abs(np.sin(rot + t))
        )
    ]

}


def compute_spiral(curve_type="log_spiral_elipse",
                   t_min=0.0, t_max=10.0, num_points=1000,
                   **curve_params):
    """
    Returns (t_vals, x_vals, y_vals) for the specified curve over t_min..t_max.
    """
    # Get the parametric functions x(t) and y(t)
    x_func, y_func = curves[curve_type]

    # Create a linspace for t
    t_vals = np.linspace(t_min, t_max, num_points)

    # Evaluate x(t), y(t)
    x_vals = x_func(t_vals, **curve_params)
    y_vals = y_func(t_vals, **curve_params)

    return t_vals, x_vals, y_vals


def plot_spiral_static():
    """
    1) Compute and plot the spiral curve (single, static plot).
    """
    # Compute spiral data
    t_vals, x_vals, y_vals = compute_spiral(
        curve_type="log_spiral_elipse",
        t_min=0,
        t_max=10,
        num_points=1000,

        # params
        a_C=1.0,
        b_C=1.0,
        L=0.1,
        rot=0.0
    )

    # Plot
    plt.figure()
    plt.plot(x_vals, y_vals, 'r-')
    plt.title("Static Log-Spiral Ellipse")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def plot_elipse():
    """
    1) Compute and plot the spiral curve (single, static plot).
    """
    # Compute spiral data
    t_vals, x_vals, y_vals = compute_spiral(
        curve_type="circle_elipse",
        t_min=0,
        t_max=10,
        num_points=1000,

        # params
        a=10.0,
        b=11.5,
        rot=0.0
    )

    # Plot
    plt.figure()
    plt.plot(x_vals, y_vals, 'r-')
    plt.title("Static Ellipse")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def plot_square():
    """
    1) Compute and plot the spiral curve (single, static plot).
    """
    # Compute spiral data
    t_vals, x_vals, y_vals = compute_spiral(
        curve_type="square",
        t_min=0,
        t_max=10,
        num_points=1000,

        # params
        a=10.0,
        b=15.0,
        rot=0.0
    )

    # Plot
    plt.figure()
    plt.plot(x_vals, y_vals, 'r-')
    plt.title("Static Ellipse")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
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
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
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
        current_a_C = abs(np.cos(2 * pi * frame / frame_bin)) * a_C + a_C
        current_b_C = abs(np.sin(2 * pi * frame / frame_bin)) * b_C + b_C


        # Compute x,y for that rotation
        _, x_vals, y_vals = compute_spiral(
            curve_type=curve_type,
            a_C=current_a_C,
            b_C=current_b_C,
            L=L,
            rot=current_rot,  # rotation changes each frame
            t_min=t_min,
            t_max=t_max
        )
        # Update the line data
        print(x_vals[-2:], y_vals[-2:])
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
    if False:
        animate_spiral_rotation(
            curve_type="log_spiral_elipse",
            a_C=1.0,
            b_C=1.0,
            L=0.015,
            rot_step=0.01,  # rotation increment
            frames=int(1E6),  # total animation frames
            t_min=0.0,
            t_max=250.0,
            interval=15
        )


        # Run the static plot demonstration
        plot_spiral_static()

    plot_square()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Dictionary of parametric curves
curves = {
    "log_spiral_elipse": [
        # x(t) = a_C * exp(L*t) * cos(rot + t)
        lambda t, a_C, L, rot: a_C * np.exp(L * t) * np.cos(rot + t),
        # y(t) = b_C * exp(L*t) * sin(rot + t)
        lambda t, b_C, L, rot: b_C * np.exp(L * t) * np.sin(rot + t)
    ]
}

def compute_spiral(curve_type="log_spiral_elipse",
                   a_C=1.0, b_C=1.0, L=0.1, rot=0.0,
                   t_min=0.0, t_max=10.0, num_points=1000):
    """
    Returns (t_vals, x_vals, y_vals) for the specified curve over t_min..t_max.
    """
    # Get the parametric functions x(t) and y(t)
    x_func, y_func = curves[curve_type]

    # Create a linspace for t
    t_vals = np.linspace(t_min, t_max, num_points)

    # Evaluate x(t), y(t)
    x_vals = x_func(t_vals, a_C, L, rot)
    y_vals = y_func(t_vals, b_C, L, rot)

    return t_vals, x_vals, y_vals

def plot_spiral_static():
    """
    1) Compute and plot the spiral curve (single, static plot).
    """
    # Compute spiral data
    t_vals, x_vals, y_vals = compute_spiral(
        curve_type="log_spiral_elipse",
        a_C=1.0,
        b_C=1.0,
        L=0.1,
        rot=0.0,
        t_min=0,
        t_max=10,
        num_points=1000
    )

    # Plot
    plt.figure()
    plt.plot(x_vals, y_vals, 'r-')
    plt.title("Static Log-Spiral Ellipse")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def animate_spiral_rotation(curve_type="log_spiral_elipse",
                            a_C=1.0, b_C=1.0, L=0.1,
                            rot_step=0.01,  # how much to increment rotation each frame
                            frames=100,     # total frames
                            t_min=0.0, t_max=10.0,
                            interval=50):
    """
    Animate the spiral while incrementing 'rot' by 'rot_step' each frame.
    """
    fig, ax = plt.subplots()
    line, = ax.plot([], [], 'r-')  # a single line object we'll update

    # Set plot bounds so we can see the curve (adjust as needed)
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_title("Rotating Log-Spiral Ellipse")

    # Optional: add a grid
    ax.grid(True)

    def init():
        # Initialize the line to empty
        line.set_data([], [])
        return (line,)

    def update(frame):
        # Current rotation = frame index * rot_step
        current_rot = frame * rot_step

        # Compute x,y for that rotation
        _, x_vals, y_vals = compute_spiral(
            curve_type=curve_type,
            a_C=a_C,
            b_C=b_C,
            L=L,
            rot=current_rot,    # rotation changes each frame
            t_min=t_min,
            t_max=t_max
        )
        # Update the line data
        line.set_data(x_vals, y_vals)
        return (line,)

    # Create the animation
    anim = FuncAnimation(
        fig,
        update,            # function called for each frame
        frames=frames,     # how many frames total
        init_func=init,    # sets up background
        blit=True,         # improves performance
        interval=interval  # delay between frames in ms
    )

    plt.show()
    return anim

# Example usage
if __name__ == "__main__":
    animate_spiral_rotation(
        curve_type="log_spiral_elipse",
        a_C=1.0,
        b_C=1.1,
        L=0.015,
        rot_step=0.01,   # rotation increment
        frames=int(1E6),      # total animation frames
        t_min=0.0,
        t_max=250.0,
        interval=5
    )

    animate_spiral_rotation(
        curve_type="log_spiral_elipse",
        a_C=1.0,
        b_C=1.5,
        L=0.075,
        rot_step=0.01,   # rotation increment
        frames=int(1E6),      # total animation frames
        t_min=0.0,
        t_max=10250.0,
        interval=5
    )

    # Run the static plot demonstration
    # plot_spiral_static()

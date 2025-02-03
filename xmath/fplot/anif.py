import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate_curve(curve_type,
                  a_C=1.0, b_C=1.0, L=0.1, rot=0.0,
                  t_min=0.0, t_max=10.0,
                  frames=200, interval=50):
    """
    Animate a parametric curve retrieved from a dictionary by `curve_type`.

    Parameters
    ----------
    curve_type : str
        The key to select the desired curve from the `curves` dictionary.
    a_C, b_C, L, rot : float
        Parameters to pass into the parametric functions for x(t) and y(t).
    t_min, t_max : float
        The range of t-values over which to animate.
    frames : int
        Number of frames in the animation (also controls the resolution).
    interval : int
        Delay between frames in milliseconds.
    """

    # Dictionary of parametric curves (add more if needed):
    curves = {
        "log_spiral_elipse": [
            # x(t)
            lambda t, a_C, L, rot: a_C * np.exp(L * t) * np.cos(rot + t),
            # y(t)
            lambda t, b_C, L, rot: b_C * np.exp(L * t) * np.sin(rot + t)
        ]
    }

    if curve_type not in curves:
        raise ValueError(f"Curve '{curve_type}' not found in the dictionary.")

    # Retrieve the x(t) and y(t) functions
    x_func, y_func = curves[curve_type]

    # Prepare t-values for the entire animation
    t_values = np.linspace(t_min, t_max, frames)

    # Create the figure and axis
    fig, ax = plt.subplots()
    # A line object that will be updated in each frame
    line, = ax.plot([], [], 'r-', animated=True)

    # (Optional) set axis limits to see the entire motion
    # You can auto-scale or choose fixed limits based on your function's range.
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_title(f"Animation: {curve_type}")

    # Initialization function for FuncAnimation
    def init():
        line.set_data([], [])
        return (line,)

    # Update function: draws the curve from t_min up to the current frame's t
    def update(frame):
        # Up to the current frame, gather partial x(t), y(t)
        current_t = t_values[:frame+1]
        x_data = [x_func(ti, a_C, L, rot) for ti in current_t]
        y_data = [y_func(ti, b_C, L, rot) for ti in current_t]

        # Update the line data
        line.set_data(x_data, y_data)
        return (line,)

    # Create the animation
    ani = FuncAnimation(
        fig,            # figure object
        update,         # update function
        frames=frames,  # total number of frames
        init_func=init, # initialization
        blit=True,      # use blitting for better performance
        interval=interval
    )

    # Display the animation
    plt.show()

    return ani


def animate_spiral_with_param_shift(
        curve_type="log_spiral_elipse",
        # Initial parameters
        a_C=1.0, b_C=1.0, L=0.1, rot=0.0,
        # New parameters after t=1000
        a_C_new=2.0, b_C_new=0.5, rot_new=np.pi / 2,
        t_min=0.0, t_mid=1000.0, t_max=2000.0,
        frames=200, interval=50
):
    """
    Animates a log-spiral ellipse from t=0 to t=1000 using the original
    parameters, then transitions those parameters from (a_C,b_C,rot)
    to (a_C_new, b_C_new, rot_new) for t in [1000..2000].

    Parameters
    ----------
    curve_type : str
        Currently only supports "log_spiral_elipse" in this demo.
    a_C, b_C, L, rot : float
        Original spiral parameters.
    a_C_new, b_C_new, rot_new : float
        Target parameters to shift to after the spiral is first drawn.
    t_min, t_mid, t_max : float
        Time boundaries for the two phases. Typically 0..1000..2000.
    frames : int
        Total number of animation frames.
    interval : int
        Milliseconds between frames.
    """

    # Dictionary of parametric curves (expand if you like)
    curves = {
        "log_spiral_elipse": [
            # x(t) = a_C * exp(L*t) * cos(rot + t)
            lambda t, aC, L, r: aC * np.exp(L * t) * np.cos(r + t),
            # y(t) = b_C * exp(L*t) * sin(rot + t)
            lambda t, bC, L, r: bC * np.exp(L * t) * np.sin(r + t)
        ]
    }

    if curve_type not in curves:
        raise ValueError(f"Curve '{curve_type}' not found in dictionary.")

    x_func, y_func = curves[curve_type]

    # Number of frames to draw the spiral fully and then shift params.
    # E.g. half of the frames for t=0..1000, half for t=1000..2000.
    half_frames = frames // 2  # integer division

    # Create figure / axis
    fig, ax = plt.subplots()
    line, = ax.plot([], [], "r-", animated=True)
    ax.set_title("Spiral from 0..1000, then param shift post-1000")

    # Decide on some limits so we can see the entire action
    ax.set_xlim(-500, 500)
    ax.set_ylim(-500, 500)

    # Initialization for FuncAnimation
    def init():
        line.set_data([], [])
        return (line,)

    def update(frame):
        """
        For each frame:
          1) Determine a 't' in [0..t_max].
          2) If t <= 1000, use the original parameters.
             If t > 1000, gradually shift them from old -> new.
          3) Plot from t_min up to current t.
        """
        # Convert the current frame to a fraction in [0..1]
        frac = frame / (frames - 1)  # from 0.0 to 1.0
        # Map this fraction to [t_min..t_max] => [0..2000] by default
        t_current = t_min + frac * (t_max - t_min)

        # 1) If t_current <= t_mid (e.g. 1000), use old params
        #    If t_current > t_mid, linearly interpolate from old to new
        if t_current <= t_mid:
            # No shift in params
            cur_a_C = a_C
            cur_b_C = b_C
            cur_rot = rot
        else:
            # fraction of how far we are between t_mid and t_max
            # e.g. t_mid=1000, t_max=2000 => t_current in [1000..2000]
            frac_shift = (t_current - t_mid) / (t_max - t_mid)  # [0..1]

            # Interpolate each param from old to new
            cur_a_C = a_C + frac_shift * (a_C_new - a_C)
            cur_b_C = b_C + frac_shift * (b_C_new - b_C)
            cur_rot = rot + frac_shift * (rot_new - rot)

        # 2) Create a set of time points from t_min..t_current to visualize
        #    so the spiral is "fully drawn" up to that time.
        if t_current <= 0:
            # If something weird, just show nothing
            time_points = np.array([0.0])
        else:
            time_points = np.linspace(t_min, t_current, 300)

        # Evaluate x(t), y(t) with the current params
        x_data = x_func(time_points, cur_a_C, L, cur_rot)
        y_data = y_func(time_points, cur_b_C, L, cur_rot)

        line.set_data(x_data, y_data)
        return (line,)

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        init_func=init,
        blit=True,
        interval=interval
    )

    plt.show()
    return anim


if __name__ == "__main__":
    """
    Example: 
    - First 100 frames go from t=0..1000 with (a_C=1, b_C=1, rot=0).
    - Next 100 frames go from t=1000..2000 linearly shifting parameters
      to (a_C=2, b_C=0.5, rot=pi/2).
    """
    animate_spiral_with_param_shift(
        curve_type="log_spiral_elipse",
        a_C=1.0, b_C=1.0, L=0.01, rot=0.0,  # Original
        a_C_new=2.0, b_C_new=0.5, rot_new=np.pi / 2,  # Shift-to
        t_min=0.0, t_mid=1000.0, t_max=2000.0,
        frames=200, interval=50
    )
    # Example usage:
    animate_curve(
        curve_type="log_spiral_elipse",
        a_C=1.0,
        b_C=1.5,
        L=0.075,
        rot=np.pi / 4,
        t_min=0.0,
        t_max=100.0,
        frames=200,
        interval=50
    )

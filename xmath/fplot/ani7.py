import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import threading

# ------------------------------------------------------------
# Apply the requested color/visual style settings globally
# ------------------------------------------------------------
plt.rcParams.update({
    'axes.facecolor': 'black',  # black background for all axes
    'axes.edgecolor': 'white',  # white border
    'axes.labelcolor': 'white',  # white axis labels
    'xtick.color': 'yellow',  # yellow tick labels
    'ytick.color': 'yellow',  # yellow tick labels
    'grid.color': 'dimgray',  # dark grey grid lines
    'figure.facecolor': 'black'  # black figure background
})


def generate_circle_points(center=(0, 0), radius=10, num_points=50):
    """
    Generate (x, y) coordinates approximating a circle via a parametric
    equation.
    Return an Nx2 NumPy array of the circle's outline.
    """
    cx, cy = center
    t = np.linspace(0, 2 * np.pi, num_points)
    x = cx + radius * np.cos(t)
    y = cy + radius * np.sin(t)
    return np.column_stack((x, y))


def generate_square_points(center=(0, 0), side_length=20):
    """
    Generate (x, y) coordinates for a square (axis-aligned) centered at
    'center'.
    Returns an Nx2 array. Here N=5 so that the last point closes the polygon.
    """
    cx, cy = center
    half = side_length / 2.0
    # (x, y) corners in clockwise or counter-clockwise order, with last =
    # first to close polygon
    points = np.array([
        [cx - half, cy - half],
        [cx + half, cy - half],
        [cx + half, cy + half],
        [cx - half, cy + half],
        [cx - half, cy - half]  # repeat first corner to close
    ])
    return points


class MovingObject:
    """
    Represents a single shape that can move around:
      - shape_coords: Nx2 NumPy array of the shape's vertices in absolute
      coords.
      - velocity: [vx, vy]
      - rotation_velocity_deg: continuous rotation speed in degrees per unit
      time
      - one_time_remaining_deg: how many degrees remain in the one-time
      rotation
      - one_time_rotation_speed_deg: speed at which we apply the one-time
      rotation
      - patch: Matplotlib Polygon patch to draw the shape.
    """

    def __init__(
            self,
            shape_coords,
            velocity=(0.0, 0.0),
            rotation_velocity_deg=0.0,
            one_time_remaining_deg=0.0,
            one_time_rotation_speed_deg=0.0,
            color='blue'
    ):
        self.shape_coords = shape_coords  # Nx2 array of absolute (x, y)
        self.velocity = list(velocity)  # [vx, vy]
        self.rotation_velocity_deg = rotation_velocity_deg
        self.one_time_remaining_deg = one_time_remaining_deg
        self.one_time_rotation_speed_deg = one_time_rotation_speed_deg

        # Create a Polygon patch for this object.
        self.patch = patches.Polygon(
            self.shape_coords,
            closed=True,
            facecolor=color,
            edgecolor='white',  # White edges to show up on black background
            alpha=0.6
        )

    def update_position(self, dt=0.1):
        """
        Update the shape's position and orientation based on:
          1) velocity => translation
          2) rotation_velocity_deg => continuous rotation
          3) one_time_remaining_deg => one-time rotation that is applied
          over time
        """

        # 1) Translate by vx*dt, vy*dt
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        # 2) Apply continuous rotation around the centroid
        total_rotation_deg = self.rotation_velocity_deg * dt

        # 3) Also apply a portion of the one-time rotation if any remains
        #    We rotate by min(one_time_rotation_speed_deg*dt, the remaining
        #    degrees).
        if abs(self.one_time_remaining_deg) > 1e-8:  # if there's some
            # rotation left
            # rotation this frame
            one_time_rotation_this_step = self.one_time_rotation_speed_deg * dt

            # if we'd overshoot the remaining, cap it
            if abs(one_time_rotation_this_step) > abs(
                    self.one_time_remaining_deg):
                one_time_rotation_this_step = abs(self.one_time_remaining_deg)

            one_time_rotation_this_step = one_time_rotation_this_step * \
                np.sign(self.one_time_remaining_deg)

            # Add the one-time rotation to the continuous rotation
            total_rotation_deg += one_time_rotation_this_step

            # Decrease the remaining rotation by the amount we used
            self.one_time_remaining_deg -= one_time_rotation_this_step

        # If total_rotation_deg != 0, rotate around centroid
        if abs(total_rotation_deg) > 1e-8:
            theta = np.radians(total_rotation_deg)
            center = self.center
            # Shift so centroid is at origin
            shifted = self.shape_coords - center
            # 2D rotation matrix
            c, s = np.cos(theta), np.sin(theta)
            R = np.array([[c, -s],
                          [s, c]])
            # Apply rotation
            rotated = (R @ shifted.T).T
            # Shift back
            self.shape_coords = rotated + center

        # Update polygon patch
        self.patch.set_xy(self.shape_coords)

    @property
    def center(self):
        """Return the centroid (approx) of the polygon."""
        return np.mean(self.shape_coords, axis=0)  # (x_mean, y_mean)


class Scene:
    """
    Holds a list of MovingObjects, updates them each frame,
    and designates a main object to center the axis on.
    """

    def __init__(self):
        self.objects = []
        self.main_object = None  # The object we center on

    def add_object(self, moving_obj, main=False):
        self.objects.append(moving_obj)
        if main:
            self.main_object = moving_obj

    def update(self, dt=0.1):
        """
        Update all objects, then return their patches
        so that we can use blitting in the animation.
        """
        for obj in self.objects:
            obj.update_position(dt=dt)
        return tuple(obj.patch for obj in self.objects)

    @property
    def main_center(self):
        """
        Return (x, y) of the main object’s center.
        If no main object is set, return (0, 0).
        """
        if self.main_object is not None:
            return self.main_object.center
        return (0.0, 0.0)


class AnimatedScene:
    """
    Ties together the Scene with Matplotlib animation
    and a background thread for user velocity + rotation input.
    """

    def __init__(self, scene):
        self.scene = scene
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')  # Keep the aspect ratio square

        # We want the axis to be roughly -100..100 in each direction,
        # but we will adjust it each frame so that the main object is centered.
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)

        # Add patches for each object to the axis
        for obj in self.scene.objects:
            self.ax.add_patch(obj.patch)

    def _input_thread(self):
        """
        Continuously reads user input and updates the *main object's*
        velocity + rotations.
        We accept either 3 or 5 comma-separated values:
          - 3 values: "vx, vy, continuousRotDeg"
          - 5 values: "vx, vy, continuousRotDeg, singleRotDeg, singleRotSpeed"

        Example inputs:
          "2, -1, 15"
          "1, 2, 10, 90, 45"
        """
        while True:
            try:
                user_input = input(
                    "Enter (vx, vy, rotDeg [, singleDeg, singleSpeed]): ")
                parts = user_input.strip().split(',')
                parts = [p.strip() for p in parts]

                if self.scene.main_object is None:
                    print(
                        "No main object set; cannot update velocity/rotation.")
                    continue

                if len(parts) == 3:
                    vx, vy, rot_deg = map(float, parts)
                    self.scene.main_object.velocity[0] = vx
                    self.scene.main_object.velocity[1] = vy
                    self.scene.main_object.rotation_velocity_deg = rot_deg
                    print(
                        f"Updated main object: v=({vx},{vy}), "
                        f"continuousRot={rot_deg} deg/unit")
                elif len(parts) == 5:
                    vx, vy, cont_rot_deg, single_deg, single_speed = map(float,
                                                                         parts)
                    mo = self.scene.main_object
                    mo.velocity[0] = vx
                    mo.velocity[1] = vy
                    mo.rotation_velocity_deg = cont_rot_deg
                    mo.one_time_remaining_deg = single_deg
                    mo.one_time_rotation_speed_deg = single_speed
                    print(f"Updated main object:\n"
                          f"  v=({vx},{vy}), continuousRot={cont_rot_deg} "
                          f"deg/unit\n"
                          f"  One-time rotate={single_deg} deg at speed="
                          f"{single_speed} deg/unit")
                else:
                    print(
                        "Error: please enter either 3 or 5 comma-separated "
                        "values.")
            except Exception as e:
                print(f"Error reading velocity/rotation: {e}. "
                      f"Format must be 'vx, vy, rotDeg' or 'vx, vy, rotDeg, "
                      f"singleDeg, singleSpeed'.")

    def start_input_thread(self):
        """
        Starts the input thread so it doesn't block the animation loop.
        """
        thread = threading.Thread(target=self._input_thread, daemon=True)
        thread.start()

    def _update_animation(self, frame):
        """
        Called by FuncAnimation each frame. Updates scene objects,
        then re-centers the axis on the main object.
        """
        patches = self.scene.update(dt=0.1)

        # Re-center the axis around the main object's center
        cx, cy = self.scene.main_center
        half_range = 100
        self.ax.set_xlim(cx - half_range, cx + half_range)
        self.ax.set_ylim(cy - half_range, cy + half_range)

        return patches

    def run(self):
        """
        Launch the Matplotlib animation. This will block until the figure is
        closed.
        """
        self.ani = animation.FuncAnimation(
            self.fig,
            self._update_animation,
            frames=None,  # None => infinite loop
            interval=50,  # ms between updates
            blit=False
        )
        plt.show()


# ------------------------------------------------------------------------
# Example usage
# ------------------------------------------------------------------------
if __name__ == "__main__":
    # Create our Scene
    scene = Scene()

    # Create a circle at (200, 100) with radius=30, velocity=(2,0)
    circle_coords = generate_circle_points(center=(200, 100), radius=30,
                                           num_points=60)
    circle_obj = MovingObject(circle_coords, velocity=(2, 0),
                              rotation_velocity_deg=0.0, color='red')
    scene.add_object(circle_obj, main=False)  # Make the circle the main object

    # Create a square at (-150, 400), side_length=50, velocity=(0,-1),
    # rotation=10 deg/unit
    square_coords = generate_square_points(center=(-150, 400), side_length=50)
    square_obj = MovingObject(square_coords, velocity=(0, -1),
                              rotation_velocity_deg=10.0, color='green')
    scene.add_object(square_obj, main=True)

    # Another circle far away
    another_circle_coords = generate_circle_points(center=(800, -300),
                                                   radius=15)
    another_circle_obj = MovingObject(another_circle_coords,
                                      velocity=(-1.5, 1.0),
                                      rotation_velocity_deg=0.0, color='blue')
    scene.add_object(another_circle_obj, main=False)

    # Create the animator, start the input thread, and run
    animator = AnimatedScene(scene)
    animator.start_input_thread()
    animator.run()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import threading


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
      - rotation_velocity_deg: rotation speed in degrees per unit time
      - patch: Matplotlib Polygon patch to draw the shape.
    """

    def __init__(self, shape_coords, velocity=(0.0, 0.0),
                 rotation_velocity_deg=0.0, color='blue'):
        self.shape_coords = shape_coords  # Nx2 array of absolute (x, y)
        self.velocity = list(velocity)  # [vx, vy]
        self.rotation_velocity_deg = rotation_velocity_deg

        # Create a Polygon patch for this object.
        self.patch = patches.Polygon(
            self.shape_coords,
            closed=True,
            facecolor=color,
            edgecolor='black',
            alpha=0.6
        )

    def update_position(self, dt=0.1):
        """
        Update the shape's position and orientation based on velocity and
        rotation_velocity_deg.
        1) Translate by vx*dt, vy*dt
        2) Rotate around centroid by rotation_velocity_deg * dt (degrees)
        """
        # 1) Translate
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        # 2) Rotate around the centroid
        if self.rotation_velocity_deg != 0.0:
            theta_deg = self.rotation_velocity_deg * dt
            theta = np.radians(theta_deg)
            center = np.mean(self.shape_coords, axis=0)

            # Shift so centroid is at origin
            shifted = self.shape_coords - center
            # Rotation matrix in 2D
            c, s = np.cos(theta), np.sin(theta)
            R = np.array([[c, -s],
                          [s, c]])
            # Apply rotation
            rotated = (R @ shifted.T).T
            # Shift back
            self.shape_coords = rotated + center

        # Finally, update polygon patch
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
        velocity + rotation.
        Expects input in the form: "vx, vy, rotation_in_degrees"
          e.g. "2, -1, 15"
        """
        while True:
            try:
                user_input = input(
                    "Enter new velocity/rotation (vx, vy, rotDeg), e.g. '2, "
                    "-1, 15': ")
                vx_str, vy_str, rot_str = user_input.strip().split(',')
                vx, vy, rot_deg = float(vx_str), float(vy_str), float(rot_str)
                if self.scene.main_object is not None:
                    self.scene.main_object.velocity[0] = vx
                    self.scene.main_object.velocity[1] = vy
                    self.scene.main_object.rotation_velocity_deg = rot_deg
                    print(
                        f"Main object updated: velocity=({vx}, {vy}), "
                        f"rotation={rot_deg} deg/unit_time")
                else:
                    print(
                        "No main object set; cannot update velocity/rotation.")
            except Exception as e:
                print(
                    f"Error reading velocity/rotation: {e}. Format must be "
                    f"'vx, vy, rotDeg'.")

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
        # Move and rotate each object
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


if __name__ == "__main__":
    # 1) Create our Scene
    scene = Scene()

    # 2) Create various objects spread around the coordinate range.
    # Example: a circle at (200, 100) with radius=30, velocity=(2,0)
    circle_coords = generate_circle_points(center=(200, 100), radius=30,
                                           num_points=60)
    circle_obj = MovingObject(circle_coords, velocity=(2, 0),
                              rotation_velocity_deg=0.0, color='red')
    scene.add_object(circle_obj, main=False)  # Make the circle the main object

    # A square at (-150, 400), side_length=50, velocity=(0,-1), rotation=10
    # deg/unit
    square_coords = generate_square_points(center=(-150, 400), side_length=50)
    square_obj = MovingObject(square_coords, velocity=(0, -1),
                              rotation_velocity_deg=10.0, color='green')
    scene.add_object(square_obj, main=True)

    # Another circle far away, with velocity=(-1.5, 1.0), rotation=0
    another_circle_coords = generate_circle_points(center=(800, -300),
                                                   radius=15)
    another_circle_obj = MovingObject(another_circle_coords,
                                      velocity=(-1.5, 1.0),
                                      rotation_velocity_deg=0.0, color='blue')
    scene.add_object(another_circle_obj, main=False)

    # 3) Create the animator, start the input thread, and run
    animator = AnimatedScene(scene)
    animator.start_input_thread()
    animator.run()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon


class PhysicsObject:
    """
    A class representing an object in 2D space that can be moved via thrust.
    """

    def __init__(self, vertices, initial_position=(0, 0),
                 initial_velocity=(0, 0), mass=1.0):
        self.position = np.array(initial_position, dtype=float)
        self.velocity = np.array(initial_velocity, dtype=float)
        self.acceleration = np.zeros(2)
        self.mass = mass
        self.thrust = np.zeros(2)
        self.vertices = np.array(vertices,
                                 dtype=float)  # vertices of the polygon
        self.max_thrust = 10.0  # maximum force magnitude available

    def apply_thrust(self, thrust_vector):
        """
        Apply a thrust vector (force). The thrust is limited to a maximum magnitude.
        """
        thrust = np.array(thrust_vector, dtype=float)
        norm = np.linalg.norm(thrust)
        if norm > self.max_thrust:
            thrust = (thrust / norm) * self.max_thrust
        self.thrust = thrust

    def update(self, dt):
        """
        Update the physics state over a time step dt.
        """
        # Calculate acceleration from F = ma.
        self.acceleration = self.thrust / self.mass
        # Update velocity and position.
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

    def get_transformed_vertices(self):
        """
        Returns the polygon vertices shifted by the current position.
        """
        return self.vertices + self.position

    def set_thrust_high(self, target):
        """
        Set a high thrust level in the direction of target.
        """
        # Example: full force in the direction of target
        direction = np.array(target, dtype=float)
        norm = np.linalg.norm(direction)
        if norm != 0:
            direction = direction / norm  # normalize
        self.apply_thrust(direction * self.max_thrust)

    def set_thrust_low(self, target, factor=0.3):
        """
        Set a lower thrust level (a fraction of max) in the direction of target.
        """
        direction = np.array(target, dtype=float)
        norm = np.linalg.norm(direction)
        if norm != 0:
            direction = direction / norm
        self.apply_thrust(direction * self.max_thrust * factor)


def run_simulation():
    # Define a simple triangle polygon (could be any shape)
    triangle_vertices = [[0, 0], [10, 0], [5, 10]]

    # Create a physics object with a polygon shape.
    obj = PhysicsObject(vertices=triangle_vertices, initial_position=(0, 0),
                        mass=10.0)

    # Define the target direction (e.g., toward (-3, 5)).
    target_direction = (-300, 500)

    dt = 0.1  # time step in seconds
    total_time = 45  # total simulation time in seconds
    steps = int(total_time / dt)

    # Storage for positions for plotting trajectory.
    trajectory = []

    # Set up matplotlib figure and axis.
    fig, ax = plt.subplots()
    ax.set_xlim(-1000, 30)
    ax.set_ylim(-30, 1000)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("2D Thrust Simulation")

    # Create a matplotlib polygon patch that will represent our object.
    poly_patch = Polygon(obj.get_transformed_vertices(), closed=True,
                         fc='blue', ec='black')
    ax.add_patch(poly_patch)

    def update_frame(frame):
        """
        Update function for animation.
        """
        # Change thrust level during simulation.
        # For example, apply high thrust during the first half and then low thrust.
        if frame < steps / 2:
            obj.set_thrust_high(target_direction)
        else:
            obj.set_thrust_low(target_direction, factor=0.3)

        # Update physics state.
        obj.update(dt)
        trajectory.append(obj.position.copy())

        # Update polygon's position.
        poly_patch.set_xy(obj.get_transformed_vertices())
        return poly_patch,

    # Run the animation.
    ani = animation.FuncAnimation(fig, update_frame, frames=steps, interval=50,
                                  blit=True, repeat=False)
    plt.show()


if __name__ == '__main__':
    run_simulation()

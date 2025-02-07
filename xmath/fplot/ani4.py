import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

class AnimatedCircle:
    def __init__(self, initial_velocity=(1.0, 1.0)):
        # Attributes
        self.velocity = list(initial_velocity)  # [vx, vy]

        # Create figure and axis
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        # Create the circle patch
        self.circle = plt.Circle((0, 0), radius=0.5, fc='blue')
        self.ax.add_patch(self.circle)

    def input_thread(self):
        """ Continuously reads user input and updates the velocity. """
        while True:
            try:
                user_input = input("Enter new velocity (vx, vy), e.g. '2, -1': ")
                vx_str, vy_str = user_input.strip().split(',')
                vx, vy = float(vx_str), float(vy_str)
                self.velocity[0] = vx
                self.velocity[1] = vy
                print(f"Velocity updated to: {self.velocity}")
            except Exception as e:
                print(f"Error reading velocity: {e}. Try again.")

    def start_input_thread(self):
        """ Starts the input thread so it doesn't block the main animation loop. """
        thread = threading.Thread(target=self.input_thread, daemon=True)
        thread.start()

    def update(self, frame_num):
        """ The update function for FuncAnimation. Moves the circle by self.velocity. """
        x, y = self.circle.center
        x += self.velocity[0] * 0.1  # scale velocity for demonstration
        y += self.velocity[1] * 0.1
        self.circle.center = (x, y)
        return (self.circle,)

    def run(self):
        """
        Sets up the FuncAnimation, then shows the plot.
        This call blocks until the figure is closed.
        """
        self.anim = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=None,   # None => infinite
            interval=50,   # ms between updates
            blit=True
        )
        plt.show()

if __name__ == "__main__":
    # Create an instance of AnimatedCircle
    animated_circle = AnimatedCircle(initial_velocity=(1.0, 1.0))

    # Start a thread for user input so it doesn't block the animation
    animated_circle.start_input_thread()

    # Run the animation
    animated_circle.run()

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

# Global/shared velocity vector
velocity = [1.0, 1.0]  # initial velocity (x=1, y=1)


def input_thread():
    """
    Wait in a loop for user input and update the velocity vector.
    Runs in a separate thread so as not to block the main animation loop.
    """
    while True:
        try:
            # Prompt user for input (example format: "2,-1")
            user_input = input("Enter new velocity (vx, vy), e.g. '2, -1': ")
            vx_str, vy_str = user_input.strip().split(',')
            vx, vy = float(vx_str), float(vy_str)

            # Update global velocity
            velocity[0] = vx
            velocity[1] = vy
            print(f"Velocity updated to: {velocity}")
        except Exception as e:
            print(f"Error reading velocity: {e}. Try again.")


def update(frame_num):
    """
    Update function for FuncAnimation.
    Moves the circle according to the current velocity vector.
    """
    global circle, velocity

    x, y = circle.center
    # Move the circle in x and y
    x += velocity[0] * 0.1  # multiply by a time-step (0.1 for demonstration)
    y += velocity[1] * 0.1
    circle.center = (x, y)

    return (circle,)


if __name__ == "__main__":
    # Start the input thread (daemon=True will let it exit when main thread
    # exits)
    thread = threading.Thread(target=input_thread, daemon=True)
    thread.start()

    # Set up the figure and axis
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    # Create a circle patch
    circle = plt.Circle((0, 0), radius=0.5, fc='blue')
    ax.add_patch(circle)

    # Create the animation
    ani = animation.FuncAnimation(
        fig,  # figure to draw in
        update,  # function that updates figure
        frames=None,  # None => infinite animation
        interval=50,  # time in ms between updates
        blit=True
    )

    plt.show()
    
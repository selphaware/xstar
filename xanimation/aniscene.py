from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

from xanimation.pscene import PhysicalScene


class AnimatedScene:
    def __init__(
            self,
            scene: PhysicalScene,
            xlim: Tuple[int, int] = (-100, 100),
            ylim: Tuple[int, int] = (-100, 100)
    ) -> None:
        self.scene: PhysicalScene = scene
        self.fig, self.ax = plt.subplots()

        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)

        for obj in self.scene.objects:
            self.ax.add_patch(obj.patch)

    def _input_thread(self):
        while True:
            try:
                user_input = input(
                    "Enter new velocity (vx, vy), e.g. '2, -1': "
                )

                vx_str, vy_str = user_input.strip().split(',')
                vx, vy = float(vx_str), float(vy_str)

                if self.scene.main_object is not None:
                    self.scene.main_object.velocity[0] = vx
                    self.scene.main_object.velocity[1] = vy
                    print(f"Main object velocity updated to: {[vx, vy]}")

                else:
                    print("No main object set; velocity not updated.")

            except Exception as e:
                print(f"Error reading velocity: {e}. Try again.")

    def start_input_thread(self):
        thread = threading.Thread(target=self._input_thread, daemon=True)
        thread.start()

    def _update_animation(self, frame):
        """
        Called by FuncAnimation each frame. Updates scene objects,
        then re-centers the axis on the main object.
        """
        # Update positions
        patches = self.scene.update(dt=0.1)

        # Re-center the axis around the main object's center
        cx, cy = self.scene.main_center
        half_range = 100  # from -100..100
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
            interval=15,  # ms between updates
            blit=False
        )
        plt.show()

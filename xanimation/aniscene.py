import sys
from typing import Tuple, List
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

from xanimation.pscene import PhysicalScene

plt.rcParams.update({
    'axes.facecolor': 'black',  # Black background for all axes
    'axes.edgecolor': 'white',  # White border
    'axes.labelcolor': 'white',  # White axis labels
    'xtick.color': 'yellow',  # White tick marks
    'ytick.color': 'yellow',  # White tick marks
    'grid.color': 'dimgray',  # Dark grey grid lines
    'figure.facecolor': 'black',  # Black figure background
})


class AnimatedScene:
    def __init__(
            self,
            scene: PhysicalScene,
            xlim: Tuple[int, int] = (-200, 200),
            ylim: Tuple[int, int] = (-100, 100),
            show_grid: bool = True,
            center_grid: bool = True
    ) -> None:
        self.scene: PhysicalScene = scene
        self.fig, self.ax = plt.subplots()

        self.center_grid: bool = center_grid

        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.xlim: List[int] = xlim
        self.ylim: List[int] = ylim

        self.ax.grid(show_grid)

        for obj in self.scene.objects:
            self.ax.add_patch(obj.patch)

        self.set_grid_to_center()

    def _input_thread(self):
        while True:
            try:
                user_input = input(
                    "Enter new velocity/rotation ("
                    "velocity-x, "
                    "velocity-y, "
                    "contRotSpeedDeg, "
                    "rotDeg, "
                    "rotSpeedDeg)> "
                )
                if user_input.lower() == "exit":
                    print("Disembarking...")
                    plt.close()
                    sys.exit(1)

                (
                    vx_str,
                    vy_str,
                    cont_rot_spd_str,
                    rot_str,
                    rot_spd_str
                ) = user_input.strip().split(',')

                vx, vy, cont_rot_spd_deg, rot_deg, rot_spd_deg = (
                    float(vx_str),
                    float(vy_str),
                    float(cont_rot_spd_str),
                    float(rot_str),
                    float(rot_spd_str)
                )

                if self.scene.main_object is not None:
                    self.scene.main_object.velocity[0] = vx
                    self.scene.main_object.velocity[1] = vy
                    self.scene.main_object.rotation_speed_deg = (
                        cont_rot_spd_deg
                    )
                    self.scene.main_object.one_time_remaining_deg = rot_deg
                    self.scene.main_object.one_time_rotation_speed_deg = (
                        rot_spd_deg
                    )
                    print(
                        f"Main object updated: velocity=({vx}, {vy})\n"
                        f"rotation={cont_rot_spd_deg} deg/unit_time\n"
                        f"one-time rotation={rot_deg} deg\n"
                        f"one-time rotation speed={rot_spd_deg} "
                        "deg/unit_time\n"
                    )
                else:
                    print(
                        "No main object set; cannot update velocity/spin."
                    )
            except Exception as e:
                print(
                    f"Error reading velocity/spin: {e}. Format must be "
                    f"'vx, vy, rotDeg'.")

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
        if self.center_grid:
            self.set_grid_to_center()

        else:
            xlim, ylim = list(self.xlim), list(self.ylim)
            x_vals = self.scene.main_object.shape_coords[:, 0]
            y_vals = self.scene.main_object.shape_coords[:, 1]

            veri_len = (ylim[1] - ylim[0])
            hori_len = (xlim[1] - xlim[0])

            if min(y_vals) <= ylim[0]:
                ylim[1] -= veri_len
                ylim[0] -= veri_len

            if max(y_vals) >= ylim[1]:
                ylim[1] += veri_len
                ylim[0] += veri_len

            if min(x_vals) <= xlim[0]:
                xlim[1] -= hori_len
                xlim[0] -= hori_len

            if max(x_vals) >= xlim[1]:
                xlim[1] += hori_len
                xlim[0] += hori_len

            self.xlim = list(xlim)
            self.ylim = list(ylim)

            self.ax.set_xlim(*self.xlim)
            self.ax.set_ylim(*self.ylim)

        return patches

    def set_grid_to_center(self):
        cx, cy = self.scene.main_center
        half_range = 100  # from -100..100
        self.xlim = [cx - half_range * 2.25, cx + half_range * 2.25]
        self.ylim = [cy - half_range * 1.25, cy + half_range * 1.25]
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)

    def run(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self._update_animation,
            frames=None,  # None => infinite loop
            interval=15,  # ms between updates
            blit=False
        )

        plt.gca().set_aspect('equal')

        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()

        plt.show()

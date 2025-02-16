import sys
from typing import Tuple, List
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mpimg
import threading
from colorama import Fore, Style
import pdb

from xanimation.pscene import PhysicalScene
from xanimation.xauxi import add_all_patches, calc_next_frame_coords

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
            center_grid: bool = True,
            full_screen: bool = False,
            enable_img_bg: bool = False,
            debug: bool = False
    ) -> None:
        self.scene: PhysicalScene = scene
        self.full_screen: bool = full_screen
        self.debug: bool = debug
        self.fig, self.ax = plt.subplots()

        # background p1
        self.star_data_x: List[float] = []
        self.star_data_y: List[float] = []
        self.scatter_stars = self.ax.scatter([], [], s=0.25,
                                             color='white')

        self.enable_img_bg: bool = enable_img_bg
        if enable_img_bg:
            self.bg_img = mpimg.imread("xanimation/background/stars.jpg")

        # END background p1

        self.center_grid: bool = center_grid

        self.ax.set_xlim(*xlim)
        self.ax.set_ylim(*ylim)
        self.xlim: List[int] = list(xlim)
        self.ylim: List[int] = list(ylim)
        self.prev_xlim = list(xlim)
        self.prev_ylim = list(ylim)

        # background p2
        if enable_img_bg:
            self.bg_handle = self.ax.imshow(
                self.bg_img,
                extent=(
                self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]),
                zorder=0
            )

        # END background p2

        self.ax.grid(show_grid)

        for obj in self.scene.objects:
            add_all_patches(obj, self.ax)

        self.set_grid_to_center()

    def _input_thread(self):
        while True:
            try:
                user_input = input(
                    Fore.LIGHTYELLOW_EX +
                    "Enter new velocity/rotation ("
                    "velocity-x, "
                    "velocity-y, "
                    "contRotSpeedDeg, "
                    "rotDeg, "
                    "rotSpeedDeg)\n> " +
                    Fore.LIGHTCYAN_EX
                )
                if user_input.lower() == "exit":
                    print(Style.RESET_ALL + "Disembarking...")
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
                    self.scene.main_object.velocity = [vx, vy]
                    self.scene.main_object.rotation_speed_deg = (
                        cont_rot_spd_deg
                    )
                    self.scene.main_object.one_time_remaining_deg = rot_deg
                    self.scene.main_object.one_time_rotation_speed_deg = \
                        rot_spd_deg
                    print(
                        Fore.GREEN +
                        f"\nMain object updated: velocity=({vx}, {vy})\n"
                        f"rotation={cont_rot_spd_deg} deg/unit_time\n"
                        f"one-time rotation={rot_deg} deg\n"
                        f"one-time rotation speed={rot_spd_deg} "
                        "deg/unit_time\n"
                    )
                else:
                    print(
                        Fore.RED +
                        "No main object set; cannot update velocity/spin." +
                        Fore.GREEN
                    )

            except Exception as e:
                print(
                    Fore.RED +
                    f"Error reading velocity/spin: {e}. Format must be "
                    f"'vx, vy, rotDeg'." +
                    Fore.GREEN
                )

            if self.debug:
                s1 = self.scene.main_object
                pdb.set_trace()

    def start_input_thread(self):
        thread = threading.Thread(target=self._input_thread, daemon=True)
        thread.start()

    def _update_animation(self, frame):
        """
        Called by FuncAnimation each frame. Updates scene objects,
        then re-centers the axis on the main object.
        """
        self.prev_xlim = list(self.xlim)
        self.prev_ylim = list(self.ylim)

        # Update positions
        patches = self.scene.update(dt=0.1)

        # Re-center the axis around the main object's center
        if self.center_grid:
            self.set_grid_to_center()

        else:
            self.set_grid_next_frame()

        self.update_background_stars()

        return (self.scatter_stars, ) + patches

    def update_background_stars(self):
        fresh = False
        if len(self.star_data_x) == 0:
            fresh = True

        x_cond, y_cond = False, False
        if not fresh:
            x_cond = (self.xlim[0] < self.prev_xlim[0]) or \
                     (self.xlim[1] > self.prev_xlim[1])
            y_cond = (self.ylim[0] < self.prev_ylim[0]) or \
                     (self.ylim[1] > self.prev_ylim[1])

        if fresh or x_cond or y_cond:
            back_star_points_x = np.random.uniform(
                self.xlim[0],
                self.xlim[1],
                50
            )
            back_star_points_y = np.random.uniform(
                self.ylim[0],
                self.ylim[1],
                50
            )
            self.star_data_x.extend(back_star_points_x)
            self.star_data_y.extend(back_star_points_y)
            self.scatter_stars.set_offsets(
                np.c_[self.star_data_x, self.star_data_y]
            )

    def set_grid_next_frame(self):
        xlim, ylim = list(self.xlim), list(self.ylim)
        x_vals = self.scene.main_object.shape_coords[:, 0]
        y_vals = self.scene.main_object.shape_coords[:, 1]
        calc_next_frame_coords(x_vals, xlim, y_vals, ylim)
        self.xlim = list(xlim)
        self.ylim = list(ylim)
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)

        if self.enable_img_bg:
            self.bg_handle.set_extent((
                self.xlim[0], self.xlim[1],
                self.ylim[0], self.ylim[1]
            ))

    def set_grid_to_center(self):
        cx, cy = self.scene.main_center
        half_range = 100  # from -100..100
        self.xlim = [cx - half_range * 2.25, cx + half_range * 2.25]
        self.ylim = [cy - half_range * 1.25, cy + half_range * 1.25]
        self.ax.set_xlim(*self.xlim)
        self.ax.set_ylim(*self.ylim)

        if self.enable_img_bg:
            self.bg_handle.set_extent((
                self.xlim[0], self.xlim[1],
                self.ylim[0], self.ylim[1]
            ))

    def run(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self._update_animation,
            frames=None,  # None => infinite loop
            interval=1,  # ms between updates
            blit=False,
            cache_frame_data=True
        )

        plt.gca().set_aspect('equal')

        if self.full_screen:
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()

        plt.show()

from typing import Tuple, List
import numpy as np
from matplotlib.patches import Polygon


class PhysicalObject:
    def __init__(
            self,
            shape_coords: np.array,
            velocity: Tuple[float, float] = (0., 0.),
            rotation_speed_deg: float = 0.,
            one_time_remaining_deg: float = 0.,
            one_time_rotation_speed_deg: float = 0.,
            color: str = "blue",
            edge_color: str = "black",
            plot_symbol: str = "r-"
    ) -> None:
        self.shape_coords: np.array = shape_coords
        self.velocity: List[float] = list(velocity)
        self.rotation_speed_deg: float = rotation_speed_deg
        self.one_time_remaining_deg: float = one_time_remaining_deg
        self.one_time_rotation_speed_deg: float = one_time_rotation_speed_deg

        self.patch: Polygon = Polygon(
            self.shape_coords,
            closed=True,
            facecolor=color,
            edgecolor=edge_color,
            alpha=0.6
        )

    def update_position(self, dt: float = 0.1) -> None:
        # update velocity
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        total_rotation_deg = self.rotation_speed_deg * dt

        # one time rotation
        if abs(self.one_time_remaining_deg) > 1e-8:
            one_time_rotation_this_step = self.one_time_rotation_speed_deg * dt

            if abs(one_time_rotation_this_step) > abs(
                    self.one_time_remaining_deg
            ):
                one_time_rotation_this_step = abs(
                    self.one_time_remaining_deg
                )

            one_time_rotation_this_step = one_time_rotation_this_step * \
                np.sign(self.one_time_remaining_deg)

            total_rotation_deg += one_time_rotation_this_step

            self.one_time_remaining_deg -= one_time_rotation_this_step

        # update rotation
        if abs(total_rotation_deg) > 1e-8:
            # theta_deg = total_rotation_deg * dt
            theta = np.radians(total_rotation_deg)
            # center = np.mean(self.shape_coords, axis=0)
            center = self.center

            # Shift so centroid is at origin
            shifted = self.shape_coords - center

            # Rotation matrix in 2D
            c, s = np.cos(theta), np.sin(theta)
            R = np.array([[c, -s],
                          [s, c]])

            # Apply rotation (multiply matrix R with vector shifted)
            rotated = (R @ shifted.T).T

            # Shift back
            self.shape_coords = rotated + center

        self.patch.set_xy(self.shape_coords)

    @property
    def center(self) -> Tuple[float, float]:
        return np.mean(self.shape_coords, axis=0)

from typing import Tuple, List, Optional
import numpy as np
from matplotlib.patches import Polygon


class PhysicalObject:
    def __init__(
            self,
            shape_coords: np.array,
            velocity: Tuple[float, float] = (0., 0.),
            _rotation_speed_deg: float = 0.,
            _one_time_remaining_deg: float = 0.,
            _one_time_rotation_speed_deg: float = 0.,
            attachments=None,
            color: str = "blue",
            edge_color: str = "black",
            plot_symbol: str = "r-"
    ) -> None:
        self.attachments: Optional[List[PhysicalObject]] = attachments

        self.shape_coords: np.array = shape_coords
        self._velocity: List[float] = list(velocity)
        self._rotation_speed_deg: float = _rotation_speed_deg
        self._one_time_remaining_deg: float = _one_time_remaining_deg
        self._one_time_rotation_speed_deg: float = _one_time_rotation_speed_deg

        self.patch: Polygon = Polygon(
            self.shape_coords,
            closed=True,
            facecolor=color,
            edgecolor=edge_color,
            alpha=0.6
        )

    @property
    def velocity(self) -> List[float]:
        return self._velocity

    @velocity.setter
    def velocity(self, in_v: List[float]) -> None:
        self._velocity = list(in_v)
        self.update_attachment_velocities()

    @property
    def rotation_speed_deg(self) -> float:
        return self._rotation_speed_deg

    @rotation_speed_deg.setter
    def rotation_speed_deg(self, in_rot: float) -> None:
        self._rotation_speed_deg = in_rot
        self.update_attachment_rotation_speed_degs()

    @property
    def one_time_remaining_deg(self) -> float:
        return self._one_time_remaining_deg

    @one_time_remaining_deg.setter
    def one_time_remaining_deg(self, in_rot: float) -> None:
        self._one_time_remaining_deg = in_rot
        self.update_attachment_one_time_rem_degs()

    @property
    def one_time_rotation_speed_deg(self) -> float:
        return self._one_time_rotation_speed_deg

    @one_time_rotation_speed_deg.setter
    def one_time_rotation_speed_deg(self, in_rot: float) -> None:
        self._one_time_rotation_speed_deg = in_rot
        self.update_attachment_one_time_rot_spd_degs()

    def update_attachment_velocities(self) -> None:
        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.velocity = self._velocity

    def update_attachment_rotation_speed_degs(self) -> None:
        if self.attachments is not None:
            for attachment in self.attachments:
                attachment._rotation_speed_deg = self._rotation_speed_deg

    def update_attachment_one_time_rem_degs(self) -> None:
        if self.attachments is not None:
            for attachment in self.attachments:
                attachment._one_time_remaining_deg = (
                    self._one_time_remaining_deg)

    def update_attachment_one_time_rot_spd_degs(self) -> None:
        if self.attachments is not None:
            for attachment in self.attachments:
                attachment._one_time_rotation_speed_deg = \
                    self._one_time_rotation_speed_deg

    def update_position(self, dt: float = 0.1) -> None:
        # update velocity
        dx = self._velocity[0] * dt
        dy = self._velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        total_rotation_deg = self._rotation_speed_deg * dt

        # one time rotation
        if abs(self._one_time_remaining_deg) > 1e-8:
            one_time_rotation_this_step = (self._one_time_rotation_speed_deg
                                           * dt)

            if abs(one_time_rotation_this_step) > abs(
                    self._one_time_remaining_deg
            ):
                one_time_rotation_this_step = abs(
                    self._one_time_remaining_deg
                )

            one_time_rotation_this_step = one_time_rotation_this_step * \
                                          np.sign(self._one_time_remaining_deg)

            total_rotation_deg += one_time_rotation_this_step

            self._one_time_remaining_deg -= one_time_rotation_this_step

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
        return np.mean(
            np.unique(self.shape_coords, axis=0),
            axis=0
        )

import time
from typing import Tuple, List, Optional
import numpy as np
from matplotlib.patches import Polygon

from xmath.xmauxi import angle_between_vectors, perpendicular


class PhysicalObject:
    def __init__(
            self,
            shape_coords: np.array,
            velocity: Tuple[float, float] = (0., 0.),
            base_indexes: Tuple[int, int] = (0, 1),
            _rotation_speed_deg: float = 0.,
            _one_time_remaining_deg: float = 0.,
            _one_time_rotation_speed_deg: float = 0.,
            is_main: bool = True,
            attachments=None,
            color: str = "blue",
            edge_color: str = "black",
            plot_symbol: str = "r-"
    ) -> None:
        self.attachments: Optional[List[PhysicalObject]] = attachments
        self.is_main: bool = is_main

        self.shape_coords: np.array = shape_coords
        self.base_indexes: Tuple[int, int] = base_indexes
        self.main_center: Optional[Tuple[float, float]] = None

        self.update_all_main_centers()

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
    def orientation_angle(self) -> float:
        angle = angle_between_vectors(
            self.orientation_direction, [0, 1]
        )

        return angle

    @property
    def orientation_direction(self) -> List[float]:
        object_north = perpendicular(
            self.shape_coords[self.base_indexes[1]] - \
            self.shape_coords[self.base_indexes[0]]
        )
        return object_north

    def rotate_then_velocity(
            self,
            tvec: List[float],
            speed: int = 100
    ) -> None:
        angle = angle_between_vectors(
            self.orientation_direction, tvec, degree=True
        ) % 360.
        print(angle)
        self.one_time_remaining_deg = angle
        self.one_time_rotation_speed_deg = speed

        self.velocity = tvec

    def update_all_main_centers(
            self,
            ncenter: Optional[Tuple[float, float]] = None
    ) -> None:
        if ncenter is None:
            if self.is_main:
                ncenter = self.center

            else:
                ncenter = self.main_center

        self.main_center = ncenter

        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.update_all_main_centers(ncenter)

    @property
    def velocity(self) -> List[float]:
        return self._velocity

    @velocity.setter
    def velocity(self, in_v: List[float]) -> None:
        self.update_all_velocities(list(in_v))  # fresh list

    @property
    def rotation_speed_deg(self) -> float:
        return self._rotation_speed_deg

    @rotation_speed_deg.setter
    def rotation_speed_deg(self, in_rot: float) -> None:
        self.update_all_rotation_speed_degs(in_rot)

    @property
    def one_time_remaining_deg(self) -> float:
        return self._one_time_remaining_deg

    @one_time_remaining_deg.setter
    def one_time_remaining_deg(self, in_rot: float) -> None:
        self.update_all_one_time_rem_degs(in_rot)

    @property
    def one_time_rotation_speed_deg(self) -> float:
        return self._one_time_rotation_speed_deg

    @one_time_rotation_speed_deg.setter
    def one_time_rotation_speed_deg(self, in_rot: float) -> None:
        self.update_all_one_time_rot_spd_degs(in_rot)

    def update_all_velocities(
            self,
            nvelocity: List[float]
    ) -> None:
        self._velocity = nvelocity

        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.update_all_velocities(nvelocity)

    def update_all_rotation_speed_degs(
            self,
            nrotation_speed_deg: float
    ) -> None:
        self._rotation_speed_deg = nrotation_speed_deg

        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.update_all_rotation_speed_degs(
                    nrotation_speed_deg
                )

    def update_all_one_time_rem_degs(
            self,
            n_one_time_remaining_deg: float
    ) -> None:
        self._one_time_remaining_deg = n_one_time_remaining_deg

        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.update_all_one_time_rem_degs(
                    n_one_time_remaining_deg
                )

    def update_all_one_time_rot_spd_degs(
            self,
            n_one_time_rot_spd_deg: float
    ) -> None:
        self._one_time_rotation_speed_deg = n_one_time_rot_spd_deg

        if self.attachments is not None:
            for attachment in self.attachments:
                attachment.update_all_one_time_rot_spd_degs(
                    n_one_time_rot_spd_deg
                )

    def update_position(self, dt: float = 0.1) -> None:
        self.update_velocity(dt)
        self.update_rotation(dt)
        self.patch.set_xy(self.shape_coords)
        self.update_all_main_centers()

    def update_rotation(self, dt):
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
            theta = np.radians(total_rotation_deg)

            if self.is_main:
                center = self.center

            else:
                center = self.main_center

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

    def update_velocity(self, dt):
        dx = self._velocity[0] * dt
        dy = self._velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

    @property
    def center(self) -> Tuple[float, float]:
        return np.mean(
            np.unique(self.shape_coords, axis=0),
            axis=0
        )

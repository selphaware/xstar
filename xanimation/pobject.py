from typing import Tuple, List
import numpy as np
from matplotlib.patches import Polygon


class PhysicalObject:
    def __init__(
            self,
            shape_coords: np.array,
            velocity: Tuple[float, float] = (0., 0.),
            spin_degree: float = 0.,
            face_color: str = "blue",
            edge_color: str = "black",
            plot_symbol: str = "r-"
    ) -> None:
        self.shape_coords: np.array = shape_coords
        self.velocity: List[float] = list(velocity)
        self.spin_degree: float = spin_degree

        self.patch: Polygon = Polygon(
            self.shape_coords,
            closed=True,
            facecolor=face_color,
            edgecolor=edge_color,
            alpha=0.6
        )

    def update_position(self, dt: float = 0.1) -> None:
        # update velocity
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        # update rotation
        if self.spin_degree != 0.0:
            theta_deg = self.spin_degree * dt
            theta = np.radians(theta_deg)
            center = np.mean(self.shape_coords, axis=0)

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

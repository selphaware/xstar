from typing import Tuple
import numpy as np
from matplotlib.patches import Polygon


class PhysicalObject:
    def __init__(
            self,
            shape_coords: np.array,
            velocity: Tuple[float, float] = (0., 0.),
            face_color: str = "blue",
            edge_color: str = "black",
            plot_symbol: str = "r-"
    ) -> None:
        self.shape_coords: np.array = shape_coords
        self.velocity = list(velocity)

        self.patch: Polygon = Polygon(
            self.shape_coords,
            closed=True,
            facecolor=face_color,
            edgecolor=edge_color,
            alpha=0.6
        )

    def update_position(self, dt: float = 0.1) -> None:
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt
        self.shape_coords[:, 0] += dx
        self.shape_coords[:, 1] += dy

        self.patch.set_xy(self.shape_coords)

    @property
    def center(self) -> Tuple[float, float]:
        return np.mean(self.shape_coords, axis=0)

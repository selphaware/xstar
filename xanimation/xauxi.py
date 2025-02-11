import math
import numpy as np
from matplotlib.patches import Polygon
from typing import List, Tuple, Any, Optional

from xanimation.pobject import PhysicalObject


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between_vectors(
        v1: List[float],
        v2: List[float],
        degree: bool = False
) -> float:
    v1 = np.array(v1)
    v2 = np.array(v2)
    dotv = np.dot(v1, v2)
    denom_v1 = np.sqrt(np.dot(v1, v1))
    denom_v2 = np.sqrt(np.dot(v2, v2))
    angle = np.arccos(dotv / (denom_v1 * denom_v2))

    if degree:
        return math.degrees(angle)

    else:
        return angle


def update_all_positions(
        pobj: PhysicalObject,
        dt: float = 0.1
) -> None:
    pobj.update_position(dt=dt)

    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            update_all_positions(attachment, dt)


def get_all_patches(
        pobj: PhysicalObject
) -> List[Polygon]:
    patches: List[Polygon] = [pobj.patch]

    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            patches.extend(get_all_patches(attachment))

    return patches


def add_all_patches(
        pobj: PhysicalObject,
        ax: Any
) -> None:
    ax.add_patch(pobj.patch)

    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            add_all_patches(attachment, ax)


def calc_next_frame_coords(x_vals, xlim, y_vals, ylim):
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


if __name__ == "__main__":
    print(angle_between_vectors([1, 1], [1, 0]))

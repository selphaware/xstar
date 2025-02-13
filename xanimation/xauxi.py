import math
import numpy as np
from matplotlib.patches import Polygon
from typing import List, Tuple, Any, Optional

from xanimation.pobject import PhysicalObject


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

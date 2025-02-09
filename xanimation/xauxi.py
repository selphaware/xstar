from matplotlib.patches import Polygon
from typing import List, Any

from xanimation.pobject import PhysicalObject


def update_attachment_positions(
        pobj: PhysicalObject,
        dt: float = 0.1
) -> None:
    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            attachment.update_position(dt=dt)

            if attachment.attachments is not None:
                for subatt in attachment.attachments:
                    update_attachment_positions(subatt, dt)


def get_attachment_patches(
        pobj: PhysicalObject
) -> List[Polygon]:
    patches: List[Polygon] = []

    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            patches.append(attachment.patch)

            if attachment.attachments is not None:
                for subatt in attachment.attachments:
                    patches.extend(get_attachment_patches(subatt))

    return patches


def add_attachment_patches(
        pobj: PhysicalObject,
        ax: Any
) -> None:
    if pobj.attachments is not None:
        for attachment in pobj.attachments:
            ax.add_patch(attachment.patch)

            if attachment.attachments is not None:
                for subatt in attachment.attachments:
                    add_attachment_patches(subatt, ax)


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

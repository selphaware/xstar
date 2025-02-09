from typing import List, Tuple, Optional

from xanimation.pobject import PhysicalObject
from xanimation.xauxi import get_attachment_patches, \
    update_attachment_positions


class PhysicalScene:
    def __init__(self):
        self.objects: List[PhysicalObject] = []
        self.main_object: Optional[PhysicalObject] = None

    def add_object(self, moving_obj: PhysicalObject, main: bool = False):
        self.objects.append(moving_obj)
        if main:
            self.main_object = moving_obj

    def update(self, dt: float = 0.1):
        for obj in self.objects:
            obj.update_position(dt=dt)
            update_attachment_positions(obj, dt)

        patches = []
        for obj in self.objects:
            patches.append(obj.patch)
            patches.extend(get_attachment_patches(obj))

        return tuple(patches)

    @property
    def main_center(self) -> Tuple[float, float]:
        if self.main_object is not None:
            return self.main_object.center
        return (0.0, 0.0)

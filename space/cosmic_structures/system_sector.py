from typing import List, Union, Optional

from xmath.structures import Z2_POS
from space.space_structures.stars import Star
from space.space_structures.planet import Planet
from ship.starship import StarShip

SECTOR_OBJECT = Union[Star, Planet, StarShip]
SECTOR_OBJECTS = List[SECTOR_OBJECT]


class SystemSector(object):
    def __init__(
            self,
            pos: Z2_POS,
            objects: Optional[SECTOR_OBJECTS] = None
    ):
        self.name: str = "System Sector " + str(pos)
        self.pos: Z2_POS = pos
        self.objects: SECTOR_OBJECTS = [] if objects is None else objects

    def get_object(self, name: str) -> SECTOR_OBJECT:
        idx_get: int = [
            idx for idx, x in enumerate(self.objects) if x.name == name
        ][0]
        return self.objects[idx_get]

    def add_object(self, obj: SECTOR_OBJECT) -> None:
        print(
            f"Adding {obj.instance_of}: {obj.name} in {self.pos} "
            f": {self.name}"
        )
        obj.position = self.pos
        self.objects.append(obj)

    def remove_object(self, name: str):
        print(f"Removing {name} from {self.name}")
        idx_remove: int = [
            idx for idx, x in enumerate(self.objects) if x.name == name
        ][0]
        self.objects.pop(idx_remove)

    @property
    def is_empty(self):
        return len(self.objects) == 0

    @property
    def position(self):
        return self.pos

    def print_info(self):
        print(self.name)
        print("==============")
        if not self.is_empty:
            for obj in self.objects:
                print(f"--- {obj.name} ---")
                obj.print_info()
                print("\n")
        else:
            print("Empty Space")

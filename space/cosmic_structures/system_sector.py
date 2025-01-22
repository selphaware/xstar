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
            name: str,
            pos: Z2_POS,
            objects: Optional[SECTOR_OBJECTS] = None
    ):
        self.name: str = name
        self.pos: Z2_POS = pos
        self.objects: SECTOR_OBJECTS = [] if objects is None else objects

    @property
    def is_empty(self):
        return self.objects is None

    @property
    def position(self):
        return self.pos

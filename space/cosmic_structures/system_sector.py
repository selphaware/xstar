from typing import List, Union, Optional

from xmath.structures import Z2_POS
from space.space_structures.stellars import StellarStructure
from space.space_structures.planet import Planet
from ship.starship import StarShip


class SystemSector(object):
    def __init__(
            self,
            name: str,
            pos: Z2_POS,
            objects: Optional[
                List[Union[StellarStructure, Planet, StarShip]]
            ] = None
    ):
        self.name: str = name
        self.pos: Z2_POS = pos
        self.objects: Optional[
            List[Union[StellarStructure, Planet, StarShip]]
        ] = objects

    @property
    def is_empty(self):
        return self.objects is None

    @property
    def position(self):
        return self.pos

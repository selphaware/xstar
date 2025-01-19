from typing import List, Union, Optional

from xmath.structures import Z2_POS
from space.space_structures.stellars import StellarObject
from space.space_structures.planet import Planet
from ship.starship import StarShip


class SystemSector(object):
    def __init__(
            self,
            name: str,
            objects: Optional[
                List[Union[StellarObject, Planet, StarShip]]
            ] = None
    ):
        self.name = name
        self.pos: Z2_POS
        self.objects = objects

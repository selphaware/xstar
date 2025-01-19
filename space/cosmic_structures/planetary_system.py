import random
from typing import List, Optional

from generic.factions import Faction
from space.space_structures.planet_types import PlanetType
from space.space_structures.stellars import StellarObject
from space.space_structures.stellar_types import StellarType
from space.space_structures.systemobj import SystemObject
from space.space_structures.planet import Planet

SPACE_MATRIX = List[List[SystemObject]]


class PlanetarySystem(object):
    def __init__(
            self,
            name: str,
            star_name: str,
            star_type: Optional[StellarType] = None,
            planet_types: Optional[List[PlanetType]] = None
    ):
        star_type: StellarType = random.choice(
            [x for x in StellarType.__members__]
        ) if star_type is None else star_type

        planet_types: List[PlanetType] = [
            random.choice([x for x in PlanetType.__members__])
            for _ in range(random.randint(5, 25))
        ] if planet_types is None else planet_types

        self.star: StellarObject = StellarObject(star_name, star_type)

        self.planets: List[Planet] = [
            Planet(
                name=f"{x.name}-{i}",
                faction=random.choice([y for y in Faction.__members__]),
                planet_type=x,
                size=random.randint(10, 500) * .01
            )
            for i, x in enumerate(planet_types)
        ]

        # TODO: PLACE IN SPIRAL

        grid_range = range(0, random.randint(1000, 100_000))
        self.grid: SPACE_MATRIX = [
            [
                SystemObject(f"System Sector {x}, {y}")
                for x in grid_range
            ]
            for y in grid_range
        ]

        # TODO: PLACE PLANETS AND STAR
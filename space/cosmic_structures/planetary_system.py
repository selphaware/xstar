import random
from typing import List, Optional, Tuple

from generic.factions import Faction
from space.space_structures.planet_types import PlanetType
from space.space_structures.stellars import StellarStructure
from space.space_structures.stellar_types import StellarType
from space.cosmic_structures.system_sector import SystemSector
from space.space_structures.planet import Planet
from xmath.pcurve import (
    generate_parametric_values,
    generate_multi_param_num_grid
)
from xmath.structures import Z2_POS

SYSTEM_SECTOR_MATRIX = List[List[SystemSector]]


class PlanetarySystem(object):
    def __init__(
            self,
            name: str,
            star_name: str,
            star: Optional[StellarStructure] = None,
            star_type: Optional[StellarType] = None,
            planets: Optional[List[Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None
    ):
        # main init
        self.name: str = name
        self.planets = None
        self.star = None
        self.shape = None
        self.origin = None

        # CODE TO BE PUT IN GENERATE BELOW

        star_type: StellarType = random.choice(
            [x for x in StellarType.__members__]
        ) if star_type is None else star_type

        planet_types: List[PlanetType] = [
            random.choice([x for x in PlanetType.__members__])
            for _ in range(random.randint(5, 25))
        ] if planet_types is None else planet_types

        self.star: StellarStructure = StellarStructure(star_name, star_type)

        self.planets: List[Planet] = [
            Planet(
                name=f"{x.name}-{i}",
                faction=random.choice([y for y in Faction.__members__]),
                planet_type=x,
                size=random.randint(10, 500) * .01
            )
            for i, x in enumerate(planet_types)
        ]

        # TODO: PLACE IN CIRCLES

        # TODO: Use PCURVE to store SystemSector

        grid_range = range(0, random.randint(1000, 100_000))
        self.grid: SYSTEM_SECTOR_MATRIX = [
            [
                SystemSector(f"System Sector {x}, {y}")
                for x in grid_range
            ]
            for y in grid_range
        ]

        # TODO: PLACE PLANETS AND STAR in Grid

    def generate(
            self,
            star_name: str,
            star: Optional[StellarStructure] = None,
            star_type: Optional[StellarType] = None,
            planets: Optional[List[Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None
    ):
        # STAR
        if star is None:
            star_type: StellarType = random.choice(
                [x for x in StellarType.__members__]
            ) if star_type is None else star_type

            self.star: StellarStructure = StellarStructure(star_name,
                                                           star_type)

        self.star = star

        # PLANETS
        if planets is None:
            if planet_types is None:
                num_planets: int = random.randint(5, 25) \
                    if num_planets is None else num_planets

                planet_types: List[PlanetType] = [
                    random.choice([x for x in PlanetType.__members__])
                    for _ in range(num_planets)
                ]

            planets: List[Planet] = [
                Planet(
                    name=f"{x.name}-{i}",
                    faction=random.choice([y for y in Faction.__members__]),
                    planet_type=x,
                    size=random.randint(10, 500) * .01
                )
                for i, x in enumerate(planet_types)
            ]

        self.planets = planets

        planet_positions = [
            generate_parametric_values(
                "circle",
                (0, 100),
                1000,
                25,
                8 / (x + 1), 0, 0
            )
            for x in range(self.num_planets)
        ]

        position_grid = generate_multi_param_num_grid(planet_positions)

        self.shape: Tuple[int, int] = (len(position_grid[0]),
                                       len(position_grid))

        self.origin: Z2_POS = (
            int(round(self.shape[0] / 2, 0)) - 1,
            int(round(self.shape[1] / 2, 0)) - 1
        )

        # TODO: place star in origin first

        grid: SYSTEM_SECTOR_MATRIX = [
            [
                # TODO: place planet on one of the positions

                SystemSector(
                    # Place planet
                    f"SYSTEM Sector {i, j}",
                    (i, j),
                    [
                        # TODO: parse the multi grid to only have unique
                        #  ints only for ints > 0 based on random positions
                        planets[position_grid[i][j] - 1]
                    ]
                ) if position_grid[i][j] > 0 \
                    else SystemSector(
                    # Empty Sector
                    f"SYSTEM Sector {i, j}",
                    (i, j),
                    None
                )

                for j, val in enumerate(col)
            ]

            for i, col in enumerate(position_grid)

            # TODO: place one planet per circle
        ]

    @property
    def num_planets(self):
        return len(self.planets)

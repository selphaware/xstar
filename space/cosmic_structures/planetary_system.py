import random
from typing import List, Optional, Dict

from generic.factions import Faction
from space.cosmic_structures.functions.calculate import (
    calculate_real_positions,
    calculate_int_positions
)
from space.cosmic_structures.functions.gridf import (
    initialise_grid,
    add_object_to_grid
)
from space.cosmic_structures.matrix_structure import SystemSectorMatrix
from space.cosmic_structures.system_sector import SystemSector, SECTOR_OBJECT
from space.space_structures.planet_types import PlanetType
from space.space_structures.stars import Star
from space.space_structures.star_types import StarType
from space.space_structures.planet import Planet
from xmath.structures import Z2_POS, R2, Z2_MATRIX, Z2


class PlanetarySystem(object):
    def __init__(
            self,
            name: str,
            star_name: str,
            star: Optional[Star] = None,
            star_type: Optional[StarType] = None,
            planets: Optional[Dict[str, Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None,
            evenly_spaced: bool = False
    ):
        print("Starting to create star system: ", name)
        # main init
        self.name: str = name + " System"
        self.planets: Optional[Dict[str, Planet]] = None
        self.planets_motion_path: Dict[str, Z2] = {}
        self.planets_motion_real_path: Dict[str, R2] = {}
        self.planets_motion_index: Dict[str, int] = {}
        self.star: Optional[Star] = None
        self.shape: Optional[Z2_POS] = None
        self.origin: Optional[Z2_POS] = None
        self.matrix: Optional[SystemSectorMatrix] = None

        self.generate_planetary_system(
            star_name,
            star,
            star_type,
            planets,
            planet_types,
            num_planets,
            evenly_spaced
        )

    def generate_planetary_system(
            self,
            star_name: str,
            star: Optional[Star] = None,
            star_type: Optional[StarType] = None,
            planets: Optional[List[Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None,
            evenly_spaced: bool = False
    ):
        # Initialise STAR
        self.initialise_star(star_name, star, star_type)

        # Initialise PLANETS
        self.initialise_planets(planets, planet_types, num_planets)

        # Calculate planet positions
        real_positions: List[R2] = calculate_real_positions(
            self.num_planets,
            evenly_spaced
        )

        # Motion Paths (int positions of planets)
        position_grid: Z2_MATRIX
        position_coords: List[Z2]
        shape: Z2_POS
        origin: Z2_POS

        position_grid, position_coords, shape, origin = (
            calculate_int_positions(real_positions)
        )

        self.shape = shape
        self.origin = origin

        # initialise grid with empty sectors
        grid_size = len(position_grid[0]), len(position_grid)
        grid: SystemSectorMatrix = initialise_grid(grid_size)

        # place star at origin
        add_object_to_grid(grid, self.origin, "Origin", self.star)

        # Assign Planet Motion Paths + PLACE PLANETS
        self.assign_planet_motion_paths(
            grid,
            position_coords,
            real_positions,
            True
        )

        self.matrix: SystemSectorMatrix = grid
        print("Shape: ", self.shape)
        print("Origin: ", self.origin)

    def assign_planet_motion_paths(
            self,
            grid: SystemSectorMatrix,
            position_coords: List[Z2],
            real_positions: List[R2],
            add_to_grid: bool = False
    ):
        # Assign planet to a motion path, and
        # assign a random position along the path
        for idx, (_name, _planet) in enumerate(self.planets.items()):
            self.planets_motion_path[_name] = position_coords[idx]
            self.planets_motion_real_path[_name] = real_positions[idx]
            self.planets_motion_index[_name] = random.randint(
                0, len(self.planets_motion_path) - 1
            )

            # add planet to sector
            sel_pos = self.planets_motion_path[_name][
                self.planets_motion_index[_name]
            ]

            if add_to_grid:
                # add to grid
                add_object_to_grid(
                    grid,
                    sel_pos,
                    f"System Sector of {_name}",
                    _planet
                )

    def initialise_planets(
            self,
            planets: Optional[Dict[str, Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None
    ):
        if planets is None:
            if planet_types is None:
                num_planets: int = random.randint(5, 25) \
                    if num_planets is None else num_planets

                planet_types: List[PlanetType] = [
                    random.choice(list(PlanetType))
                    for _ in range(num_planets)
                ]

            planets: Dict[str, Planet] = {
                f"{str(x)}-{i}": Planet(
                    name=f"{str(x)}-{i}",
                    faction=random.choice([y for y in Faction.__members__]),
                    planet_type=x,
                    size=random.randint(10, 500) * .01,
                )
                for i, x in enumerate(planet_types)
            }

        print(f"Created {num_planets} planets")
        self.planets = planets

    def initialise_star(
            self,
            star_name: str,
            star: Optional[Star] = None,
            star_type: Optional[StarType] = None,
    ):
        if star is None:
            star_type: StarType = random.choice(list(StarType)) \
                if (star_type is None) else star_type

            star: Star = Star(
                star_name,
                star_type
            )

        print(f"Created star: {star.name}, Type: {star_type}")
        self.star = star

    @property
    def num_planets(self):
        return len(self.planets)

    def get_sector(self, _pos: Z2_POS) -> SystemSector:
        return self.matrix.get_sector(_pos)

    def get_object(self, _pos: Z2_POS, name: str) -> SECTOR_OBJECT:
        return self.matrix.get_object(_pos, name)

    def print_info(self):
        item_objs = (
            [
                [
                    (i.name,
                     str(i.instance_of),
                     y.position) for i in y.objects
                ]
                for x in self.matrix.sectors
                for y in x if len(y.objects) > 0
            ]
        )

        for item_obj in item_objs:
            print(item_obj)

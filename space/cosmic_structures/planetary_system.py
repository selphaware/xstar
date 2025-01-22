import random
from typing import List, Optional, Tuple

from generic.factions import Faction
from space.cosmic_structures.grid_structure import SystemSectorMatrix
from space.space_structures.planet_types import PlanetType
from space.space_structures.stars import Star
from space.space_structures.star_types import StarType
from space.space_structures.planet import Planet
from xmath.pcurve import (
    generate_parametric_values,
    generate_multi_param_num_grid
)
from xmath.structures import Z2_POS, R2, Z2_MATRIX, Z2


class PlanetarySystem(object):
    def __init__(
            self,
            name: str,
            star_name: str,
            star: Optional[Star] = None,
            star_type: Optional[StarType] = None,
            star_motion_decay: Optional[int] = None,
            planets: Optional[List[Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None,
            evenly_spaced: bool = False
    ):
        # main init
        self.name: str = name
        self.planets: Optional[List[Planet]] = None
        self.star: Optional[Star] = None
        self.real_positions: Optional[List[R2]] = None
        self.int_positions: Optional[Z2_MATRIX] = None
        self.position_coords: Optional[List[Z2]] = None
        self.shape: Optional[Tuple[int, int]] = None
        self.origin: Optional[Tuple[int, int]] = None
        self.matrix: Optional[SystemSectorMatrix] = None

        self.generate_planetary_system(
            star_name,
            star,
            star_type, star_motion_decay,
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
            star_motion_decay: Optional[int] = None,
            planets: Optional[List[Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None,
            evenly_spaced: bool = False
    ):
        # Initialise STAR
        self.initialise_star(star_name, star, star_type, star_motion_decay)

        # Initialise PLANETS
        self.initialise_planets(planets, planet_types, num_planets)

        # Calculate planet positions
        self.calculate_real_positions(evenly_spaced)

        # Motion Paths (int positions of planets)
        self.calculate_int_positions()

        # initialise grid with empty sectors
        system_size: Z2_POS = (
            len(self.int_positions[0]),
            len(self.int_positions)
        )
        grid: SystemSectorMatrix = SystemSectorMatrix(system_size)

        # place star at origin
        grid.set_sector_name(self.origin, "Origin")
        grid.add_sector_object(self.origin, self.star)

        # PLACE PLANETS
        planet_motion_paths = {
            self.planets[idx].name: planet_path
            for idx, planet_path in enumerate(self.position_coords)
        }

        _planets = {
            _planet.name: _planet
            for _planet in self.planets
        }

        for planet_name, planet_path in planet_motion_paths.items():
            sel_pos: Z2_POS = random.choice(planet_path)
            grid.set_sector_name(sel_pos,
                                 f"System Sector of {planet_name}")
            grid.add_sector_object(sel_pos, _planets[planet_name])

        self.matrix: SystemSectorMatrix = grid

    def calculate_int_positions(self):
        position_grid = generate_multi_param_num_grid(
            self.real_positions
        )
        self.int_positions = position_grid

        self.position_coords: List[Z2] = [
            [
                (int(round(x, 0)), int(round(y, 0)))
                for (x, y) in prp
            ]
            for prp in self.real_positions
        ]

        self.shape: Tuple[int, int] = (len(self.int_positions[0]),
                                       len(self.int_positions))

        self.origin: Z2_POS = (
            int(round(self.shape[0] / 2, 0)) - 1,
            int(round(self.shape[1] / 2, 0)) - 1
        )

    def calculate_real_positions(self, evenly_spaced: bool = False):
        time_range = (0, 100)
        num_points = 1000
        factor = 25
        planet_range = range(1, self.num_planets + 1)
        dist_metric = lambda rator, denom: rator / denom \
            if evenly_spaced else rator - denom

        planet_real_positions = [
            generate_parametric_values(
                "circle",
                time_range,
                num_points,
                factor,
                r=dist_metric(18, x), hs=0, vs=0
            )
            for x in planet_range
            if x % 2 == 1
        ]

        planet_real_positions.extend([
            generate_parametric_values(
                "elipse",
                time_range,
                num_points,
                factor,
                a=dist_metric(20, x), b=dist_metric(16, x),
                hs=0, vs=0
            )
            for x in planet_range
            if x % 2 == 0
        ])

        self.real_positions = planet_real_positions

    def initialise_planets(self, planets, planet_types, num_planets):
        if planets is None:
            if planet_types is None:
                num_planets: int = random.randint(5, 25) \
                    if num_planets is None else num_planets

                planet_types: List[PlanetType] = [
                    random.choice(list(PlanetType))
                    for _ in range(num_planets)
                ]

            planets: List[Planet] = [
                Planet(
                    name=f"{str(x)}-{i}",
                    faction=random.choice([y for y in Faction.__members__]),
                    planet_type=x,
                    size=random.randint(10, 500) * .01
                )
                for i, x in enumerate(planet_types)
            ]

        self.planets = planets

    def initialise_star(
            self,
            star_name: str,
            star: Optional[Star] = None,
            star_type: Optional[StarType] = None,
            star_motion_decay: Optional[int] = None
    ):
        if star is None:
            star_type: StarType = random.choice(
                [x for x in StarType.__members__]
            ) if star_type is None else star_type

            star: Star = Star(
                star_name,
                star_type,
                100 if star_motion_decay is None else star_motion_decay
            )

        self.star = star

    @property
    def num_planets(self):
        return len(self.planets)

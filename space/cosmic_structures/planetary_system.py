import random
from typing import List, Optional, Dict, Union

from generic.factions import Faction
from ship.starship import StarShip
from space.cosmic_structures.functions.calculate import (
    calculate_real_positions,
    calculate_int_positions, get_vector_between_positions,
    get_distance_between_positions, add_vectors
)
from space.cosmic_structures.matrix_structure import SystemSectorMatrix
from space.cosmic_structures.system_sector import (SystemSector,
                                                   SECTOR_OBJECT, \
                                                   SECTOR_OBJECTS)
from space.space_structures.planet_types import PlanetType
from space.space_structures.stars import Star
from space.space_structures.star_types import StarType
from space.space_structures.planet import Planet
from xmath.structures import Z2_POS, R2, Z2_MATRIX, Z2, R2_POS
from xmath.xrandom import random_int_generator


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
        self.epoch: int = 1
        self.name: str = name + " System"
        self.planets: Optional[Dict[str, Planet]] = None
        self.objects_path: Dict[str, Z2] = {}
        self.objects_real_path: Dict[str, R2] = {}
        self.objects_position_index: Dict[str, int] = {}
        self.star: Optional[Star] = None
        self.shape: Optional[Z2_POS] = None
        self.origin: Optional[Z2_POS] = None
        self.matrix: Optional[SystemSectorMatrix] = None
        self.ships: Dict[str, StarShip] = {}

        self.generate_planetary_system(
            star_name,
            star,
            star_type,
            planets,
            planet_types,
            num_planets,
            evenly_spaced
        )

    @property
    def num_planets(self) -> int:
        return len(self.planets)

    def num_ships(self) -> int:
        return len(self.ships)

    @property
    def star_position(self) -> Z2_POS:
        return self.object_positions[self.star.name]

    @property
    def object_positions(self) -> Dict[str, Z2_POS]:
        ppos: Dict[str, Z2_POS] = {
            _name: _path[self.objects_position_index[_name]]
            for _name, _path in self.objects_path.items()
        }

        return ppos

    @property
    def object_real_positions(self) -> Dict[str, R2_POS]:
        ppos: Dict[str, R2_POS] = {
            _name: _path[self.objects_position_index[_name]]
            for _name, _path in self.objects_real_path.items()
        }

        return ppos

    @property
    def next_object_positions(self) -> Dict[str, Z2_POS]:
        ppos: Dict[str, Z2_POS] = {
            _name: _path[
                self.objects_position_index[_name] + 1 % len(
                    self.objects_path[_name]
                )
                ]
            for _name, _path in self.objects_path.items()
        }

        return ppos

    @property
    def next_object_real_positions(self) -> Dict[str, R2_POS]:
        ppos: Dict[str, R2_POS] = {
            _name: _path[
                self.objects_position_index[_name] + 1 % len(
                    self.objects_path[_name]
                )
                ]
            for _name, _path in self.objects_real_path.items()
        }

        return ppos

    @property
    def next_object_vectors(self) -> Dict[str, Z2_POS]:
        nvecs: Dict[str, Z2_POS] = {
            _name:
                (
                    self.next_object_positions[_name][0] -
                    self.object_positions[_name][0],

                    self.next_object_positions[_name][1] -
                    self.object_positions[_name][1]
                )
            for _name in self.object_names
        }

        return nvecs

    @property
    def next_object_real_vectors(self) -> Dict[str, R2_POS]:
        nvecs: Dict[str, R2_POS] = {
            _name: get_vector_between_positions(
                self.next_object_real_positions[_name],
                self.object_real_positions[_name]
            )
            for _name in self.object_names
        }

        return nvecs

    @property
    def motion_decay(self) -> int:
        return self.star.motion_decay

    @property
    def planet_names(self) -> List[str]:
        return [x for x in self.planets.keys()]

    @property
    def ship_names(self) -> List[str]:
        return [x for x in self.ships.keys()]

    @property
    def object_names(self) -> List[str]:
        return [self.star.name] + self.planet_names + self.ship_names

    @property
    def objects(self) -> Dict[str, SECTOR_OBJECT]:
        dret: Dict[str, SECTOR_OBJECT] = {
            k: v for k, v in self.planets.items()
        }

        dret[self.star.name] = self.star

        dret.update({
            k: v for k, v in self.ships.items()
        })

        return dret

    def add_ship(
            self,
            ship: StarShip,
            _pos: Union[Z2_POS, R2_POS],
            refresh_grid: bool = False
    ) -> None:
        print(f"Adding star ship {ship.name} to {_pos}")
        self.ships[ship.name] = ship
        self.objects_path[ship.name] = [_pos]
        self.objects_position_index[ship.name] = 0
        self.objects_real_path[ship.name] = [_pos]
        ship.position = _pos

        if refresh_grid:
            self.matrix.add_sector_object(_pos, ship)

    def get_objects_from_position(self, position: Z2_POS) -> SECTOR_OBJECTS:
        objects: SECTOR_OBJECTS = [
            self.objects[obj_name]
            for obj_name, curr_pos in self.object_positions.items()
            if position == curr_pos
        ]

        return objects

    def get_object_names_from_position(
            self, position: Z2_POS
    ) -> List[str]:
        object_names: List[str] = [
            obj_name
            for obj_name, curr_pos in self.object_positions.items()
            if position == curr_pos
        ]

        return object_names

    def get_vector_between_objects(self, name1: str, name2: str) -> Z2_POS:
        return get_vector_between_positions(
            self.object_positions[name1],
            self.object_positions[name2]
        )

    def get_real_vector_between_objects(
            self, name1: str, name2: str
    ) -> Z2_POS:
        return get_vector_between_positions(
            self.object_real_positions[name1],
            self.object_real_positions[name2]
        )

    def get_distance_between_objects(
            self, name1: str, name2: str
    ) -> int:
        return get_distance_between_positions(
            self.object_positions[name1],
            self.object_positions[name2],
            roundit=True
        )

    def get_real_distance_between_objects(
            self, name1: str, name2: str
    ) -> float:
        return get_distance_between_positions(
            self.object_real_positions[name1],
            self.object_real_positions[name2],
            roundit=False
        )

    def turn(self, refresh_grid: bool = False):
        # move all objects on next motion path
        if (self.epoch > 0) and (self.epoch % self.star.motion_decay == 0):
            # move planets if motion decay in play
            self.turn_planets(refresh_grid)

        # move ships along their motion paths
        self.turn_ships(refresh_grid)

        self.epoch += 1

    def turn_ships(self, refresh_grid: bool = False):
        for _ship in self.ship_names:
            curr_pos = self.object_positions[_ship]

            if refresh_grid:
                self.matrix.remove_sector_object(
                    curr_pos,
                    _ship
                )

            new_pos = add_vectors(
                curr_pos,
                self.ships[_ship].motion_vector
            )
            self.objects_path[_ship] = [new_pos]
            self.ships[_ship].position = new_pos

            if refresh_grid:
                self.matrix.add_sector_object(
                    new_pos,
                    self.ships[_ship]
                )

    def turn_planets(self, refresh_grid: bool = False):
        for _planet in self.planet_names:
            if refresh_grid:
                curr_pos = self.object_positions[_planet]
                self.matrix.remove_sector_object(
                    curr_pos,
                    _planet
                )

            self.objects_position_index[_planet] += 1
            self.objects_position_index[_planet] %= len(
                self.objects_path[_planet]
            )
            new_pos = self.object_positions[_planet]

            if refresh_grid:
                self.matrix.add_sector_object(
                    new_pos,
                    self.planets[_planet]
                )

    # TODO: PLOT POSITIONS + VECTOR ARROWS !!!!!

    # TODO: MULTIPY ON ADDING LARGE NUM OF OBJECTS

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
        self.matrix: SystemSectorMatrix = SystemSectorMatrix(grid_size)

        # place star at origin
        self.matrix.add_sector_object(self.origin, self.star)

        # Assign Planet Motion Paths + PLACE PLANETS
        self.assign_planet_motion_paths(
            position_coords,
            real_positions,
            True
        )

        # add star to motion path variables
        self.objects_path[self.star.name] = [self.origin]
        self.objects_real_path[self.star.name] = [(0., 0.)]
        self.objects_position_index[self.star.name] = 0

        print("Shape: ", self.shape)
        print("Origin: ", self.origin)

    def assign_planet_motion_paths(
            self,
            position_coords: List[Z2],
            real_positions: List[R2],
            add_to_grid: bool = False
    ):
        # Assign planet to a motion path, and
        # assign a random position along the path
        for idx, (_name, _planet) in enumerate(self.planets.items()):
            self.objects_path[_name] = position_coords[idx]
            self.objects_real_path[_name] = real_positions[idx]

            rand_int_gen = random_int_generator(
                0, len(self.objects_path[_name]) - 1
            )
            self.objects_position_index[_name] = next(rand_int_gen)

            # add planet to sector
            sel_pos = self.objects_path[_name][
                self.objects_position_index[_name]
            ]

            if add_to_grid:
                # add to grid
                self.matrix.add_sector_object(sel_pos, _planet)

    def initialise_planets(
            self,
            planets: Optional[Dict[str, Planet]] = None,
            planet_types: Optional[List[PlanetType]] = None,
            num_planets: Optional[int] = None
    ):
        if planets is None:
            if planet_types is None:
                rand_int_gen = random_int_generator(5, 25)
                num_planets: int = next(rand_int_gen) \
                    if num_planets is None else num_planets

                rand_choice_gen = random_int_generator(
                    0, len(list(PlanetType)) - 1
                )
                planet_types: List[PlanetType] = [
                    list(PlanetType)[next(rand_choice_gen)]
                    for _ in range(num_planets)
                ]

            name_trans = lambda _x, _i, _n: f"{str(_x)}-{_i} ({_n})"

            rand_int_gen = random_int_generator(5000, 500_000)
            rand_choice_gen = random_int_generator(
                0, len(list(Faction)) - 1
            )
            planets: Dict[str, Planet] = {
                name_trans(x, i, self.name): Planet(
                    name=name_trans(x, i, self.name),
                    faction=list(Faction)[next(rand_choice_gen)],
                    planet_type=x,
                    size=next(rand_int_gen) * .001,
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
            rand_choice_gen = random_int_generator(
                0, len(list(StarType)) - 1
            )
            star_type: StarType = list(StarType)[next(rand_choice_gen)] \
                if (star_type is None) else star_type

            star: Star = Star(
                star_name,
                star_type
            )

        print(f"Created star: {star.name}, Type: {star_type}")
        self.star = star

    def get_sector(self, _pos: Z2_POS) -> SystemSector:
        return self.matrix.get_sector(_pos)

    def get_object(self, _pos: Z2_POS, name: str) -> SECTOR_OBJECT:
        return self.matrix.get_object(_pos, name)

    def print_info(self, full: bool = False):
        item_objs = [
            [
                (
                    w.name,
                    str(w.instance_of),
                    (i, j)
                ) for w in x.objects
            ]
            for j, y in enumerate(self.matrix.sectors)
            for i, x in enumerate(y)
            if len(x.objects) > 0 or full
        ]

        for item_obj in item_objs:
            print(item_obj, end=" " if full else "\n")

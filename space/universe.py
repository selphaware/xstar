from typing import List, Dict, Any

from xmath.generate_universe import generate_universe_parametric_values
from xmath.structures import UNIVERSE_STRUCT, R2, R2_POS


class Universe(object):
    def __init__(
            self,
            num_galaxies: int = 36,
            num_systems: int = 20,
            num_planet_orbits: int = 16,
            rand_size_range_limit: int = 5,
            galaxy_distance: float = 10.,
            num_black_holes: int = 10
    ):
        self.universe_positions: UNIVERSE_STRUCT = (
            generate_universe_parametric_values(
                num_galaxies, num_systems, num_planet_orbits,
                rand_size_range_limit, galaxy_distance,
                num_black_holes
            )
        )

        self.epoch: int = 1

    @property
    def galaxy_names(self) -> List[str]:
        return [str(x) for x in self.universe_positions.keys()]

    @property
    def galaxy_paths(self) -> Dict[str, R2]:
        _gp: Dict[str, R2] = {}
        for gname, galaxy in self.universe_positions.items():
            _gp[gname] = galaxy['motion_path']
        return _gp

    @property
    def star_names(self) -> List[str]:
        return [str(x) for x in self.stars.keys()]

    @property
    def black_hole_names(self) -> List[str]:
        return [str(x) for x in self.black_holes.keys()]

    @property
    def planet_names(self) -> List[str]:
        return [str(x) for x in self.planets.keys()]

    @property
    def stars(self) -> Dict[str, R2_POS]:
        _stars: Dict[str, R2_POS] = {}
        for gname, galaxy in self.universe_positions.items():
            for sname, system in galaxy['star_systems'].items():
                if not system['is_centre']:
                    _stars[system['star_name']] = system['origin'][0]
        return _stars

    @property
    def black_holes(self) -> Dict[str, R2_POS]:
        _stars: Dict[str, R2_POS] = {}
        for gname, galaxy in self.universe_positions.items():
            for sname, system in galaxy['star_systems'].items():
                if system['is_centre']:
                    _stars[system['star_name']] = system['origin'][0]
        return _stars

    @property
    def planets(self) -> Dict[str, Any]:
        _planets: Dict[str, Any] = {}
        for gname, galaxy in self.universe_positions.items():
            for sname, system in galaxy['star_systems'].items():
                for planet_name, planet_position in system['planets'].items():
                    _planets[planet_name] = planet_position
        return _planets

    @property
    def star_positions(self) -> R2:
        return [x for x in self.stars.values()]

    @property
    def black_hole_positions(self) -> R2:
        return [x for x in self.black_holes.values()]

    @property
    def planet_positions(self) -> Dict[str, R2]:
        return {
            w:
            x['position'][0] for w, x in self.planets.items()
        }

    @property
    def planet_paths(self) -> Dict[str, R2]:
        return {
            w:
            x['motion_path'] for w, x in self.planets.items()
        }

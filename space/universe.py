from typing import List, Dict

from xmath.generate_universe import generate_universe_parametric_values
from xmath.structures import UNIVERSE_STRUCT, R2, R2_POS


class Universe(object):
    def __init__(
            self,
            num_galaxies: int = 36,
            num_systems: int = 20,
            num_planet_orbits: int = 16
    ):
        self.universe_positions: UNIVERSE_STRUCT = (
            generate_universe_parametric_values(
                num_galaxies, num_systems, num_planet_orbits
            )
        )

        self.epoch: int = 1

    @property
    def galaxy_names(self) -> List[str]:
        return [str(x) for x in self.universe_positions.keys()]

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
    def star_positions(self) -> R2:
        return [x for x in self.stars.values()]

    @property
    def black_hole_positions(self) -> R2:
        return [x for x in self.black_holes.values()]

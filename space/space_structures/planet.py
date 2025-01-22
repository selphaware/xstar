from typing import List, Optional

from generic.factions import Faction
from space.space_structures.planet_types import PlanetType
from xmath.structures import Z2


class Country(object):
    def __init__(
            self,
            name: str,
            morale: float = .65,
            population: int = 1E6,
            food: int = 1E6,
            energy: int = 1E6
    ):
        self.name: str = name
        self.morale: float = morale
        self.population = population
        self.food = food
        self.energy = energy


class Planet(object):
    def __init__(
            self,
            name: str,
            faction: Faction,
            planet_type: PlanetType,
            size: float = 1.0,
            motion_path: Optional[Z2] = None,
            motion_decay: Optional[int] = None
    ):
        self.name = name
        self.faction: Faction = faction
        self.planet_type: PlanetType = planet_type
        self.motion_path = motion_path,
        self.motion_decay = motion_decay

        countries: List[Country] = []
        if planet_type.supports_life:
            num_countries = 0
            if planet_type.habitability == "Habitable":
                num_countries = 250 * size

            elif planet_type.habitability == "Habitable with adaption":
                num_countries = 30 * size

            elif planet_type.habitability == "Super Habitable":
                num_countries = 1500 * size

            elif planet_type.habitability == "Partially Habitable":
                num_countries = 100 * size

            num_countries = int(round(num_countries, 0))

            countries: List[Country] = [
                Country(str(i)) for i in range(num_countries)
            ]

        self.countries: List[Country] = countries

    @property
    def population(self) -> int:
        return sum([x.population for x in self.countries])

    @property
    def energy(self) -> int:
        return sum([x.energy for x in self.countries])

    @property
    def food(self) -> int:
        return sum([x.food for x in self.countries])

    @property
    def morale(self) -> float:
        return sum([x.morale for x in self.countries]) / len(self.countries)

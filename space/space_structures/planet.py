from typing import List, Union
from math import pi

from generic.factions import Faction
from space.space_structures.planet_types import PlanetType
from xmath.structures import Z2_POS


class Country(object):
    def __init__(
            self,
            name: str,
            morale: Union[float, str] = .65,
            population: int = 1E6,
            food: int = 1E6,
            energy: int = 1E6
    ):
        self.name: str = name
        self.morale: Union[float, str] = morale
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
    ):
        self.name = name
        self.faction: Faction = faction
        self.instance_of: PlanetType = planet_type
        self.position: Z2_POS = (0, 0)
        self.size = size

        countries: List[Country] = []
        if planet_type.supports_life:
            num_countries = 0
            if planet_type.habitability == "Habitable":
                num_countries = 250 * size

            elif planet_type.habitability == "Habitable with adaptation":
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
    def morale(self) -> Union[float, str]:
        if self.num_countries > 0:
            return sum(
                [x.morale for x in self.countries]
            ) / len(self.countries)
        else:
            return "N/A"

    @property
    def num_countries(self) -> int:
        return len(self.countries)

    @property
    def radius(self) -> float:
        return self.size * 10E5

    @property
    def volume(self) -> float:
        return (4 / 3) * pi * self.radius ** 3

    def print_info(self):
        print(f"Planet Name: {self.name}")
        print(f"Position: {self.position}")
        print(f"Population: {self.population}")
        print(f"Num. Countries: {self.num_countries}")
        print(f"Food: {self.food}")
        if isinstance(self.morale, float):
            print(f"Morale: {self.morale * 100} %")
        elif isinstance(self.morale, str):
            print(f"Morale: {self.morale}")
        print(f"Energy: {self.energy}")
        print(f"Size Radius: {self.radius} KM")
        print(f"Size Radius: {self.volume} KM^3")

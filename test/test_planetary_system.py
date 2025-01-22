from space.cosmic_structures.planetary_system import PlanetarySystem
from space.space_structures.star_types import StarType

import pdb


def test_planetary_system_generation():
    print("Generating star system: Alice-1 ...")
    ps: PlanetarySystem = PlanetarySystem(
        # system info
        "Alice-1",

        # star
        "Nixiru",
        None,
        StarType.Star,
        100,

        # planets
        None,
        None,
        16,
        True
    )
    print("Alice-1 star system has been generated.\n")

    pdb.set_trace()

if __name__ == "__main__":
    test_planetary_system_generation()

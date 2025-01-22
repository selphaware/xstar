from space.cosmic_structures.planetary_system import PlanetarySystem
from space.space_structures.star_types import StarType

import pdb


def test_planetary_system_generation():
    print("Generating star system: Alice-1 ...")
    ps: PlanetarySystem = PlanetarySystem(
        # system info
        "Alice-1",

        # star
        "Nixiru Star",
        None,
        StarType.Star,
        100,

        # planets
        None,
        None,
        16,
        True
    )
    # print([y.objects for x in ps.matrix.sectors for y in x])

    ps.print_system_items_positions()

    print(f"\nShape: {ps.shape}, Origin: {ps.origin}")

    print("\nAlice-1 star system has been generated.\n")

    pdb.set_trace()

    print("\nDestroying Alice-1 star system...")


if __name__ == "__main__":
    test_planetary_system_generation()

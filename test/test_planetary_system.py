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

        # planets
        None,
        None,
        16,
        True
    )
    # print([y.objects for x in ps.matrix.sectors for y in x])
    wout = [
        y.objects[0].name
        if len(y.objects)
        else ""
        for x in ps.matrix.sectors for y in x
    ]
    with open("test/space.out", "w") as ff:
        ff.write(str(wout))

    # ps.print_info()

    print(f"\nShape: {ps.shape}, Origin: {ps.origin}")

    print("\nAlice-1 star system has been generated [ps].\n")

    print("Creating a black hole system...")
    bs = PlanetarySystem(
        "PX3", "PX3", None, StarType.BlackHole,
        num_planets=50, evenly_spaced=True
    )
    print("Completed [ps, bs].")

    pdb.set_trace()

    print("\nDestroying Alice-1 and Black Hole star systems...")


if __name__ == "__main__":
    test_planetary_system_generation()

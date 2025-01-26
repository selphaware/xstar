from generic.factions import Faction
from ship.ship_types.engines import WarpEngine, ImpulseEngine
from ship.ship_types.missions import Mission
from ship.ship_types.shields import Shields
from ship.ship_types.weapons import PrimaryWeapon, SecondaryWeapon
from ship.starship import StarShip
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
        num_planets=35, evenly_spaced=True
    )
    print("Completed [ps, bs].\n\n")

    cs: PlanetarySystem = PlanetarySystem(
        # system info
        "Chronos-1",

        # star
        "Worf",
        None,
        StarType.RedGiant,

        # planets
        None,
        None,
        3,
        False
    )

    cs.add_ship(
        StarShip(
            "Shuttlecraft-0",
            Faction.Federation,
            "A-001",
            "Usman Ahmad",
            Mission.Scientific,
            100,
            Shields.Tachyon,
            True,
            [
                PrimaryWeapon.PhaserArray,
                PrimaryWeapon.DisruptorCannons
            ],
            [
                SecondaryWeapon.QuantumMines,
                SecondaryWeapon.PolaronBursts
            ],
            WarpEngine.StandardWarpDrive,
            ImpulseEngine.FusionDrive
        ),
        cs.object_positions[cs.planet_names[0]],
        True
    )

    shuttle = cs.ships["Shuttlecraft-0 (A-001)"]

    cs.print_info()

    pdb.set_trace()

    print("\nDestroying star systems...")


if __name__ == "__main__":
    test_planetary_system_generation()

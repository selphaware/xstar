from enum import Enum


class StellarType(Enum):
    Star = (
        "A luminous ball of gas, mostly hydrogen and helium, undergoing "
        "nuclear fusion",
        80,
        0.5,
    )
    BlackHole = (
        "A region of spacetime with gravity so strong that nothing can "
        "escape it",
        10,
        1.0,
    )
    NeutronStar = (
        "A compact stellar remnant of a massive star after a supernova",
        60,
        0.8,
    )
    Pulsar = (
        "A rapidly spinning neutron star emitting beams of electromagnetic "
        "radiation",
        70,
        0.7,
    )
    WhiteDwarf = (
        "A dense, cooling remnant of a low-mass star",
        40,
        0.3,
    )
    RedGiant = (
        "A large, bright star in a late stage of stellar evolution",
        50,
        0.4,
    )
    Supernova = (
        "A powerful explosion marking the death of a massive star",
        100,
        0.6,
    )
    Quasar = (
        "An extremely energetic active galactic nucleus powered by a "
        "supermassive black hole",
        100,
        0.9,
    )
    Protostar = (
        "A young star in the early stage of formation",
        30,
        0.2,
    )
    BrownDwarf = (
        "A substellar object not massive enough for nuclear fusion",
        20,
        0.15,
    )
    Magnetar = (
        "A type of neutron star with an extremely powerful magnetic field",
        70,
        0.85,
    )
    BinaryStar = (
        "A system of two stars orbiting a common center of mass",
        90,
        0.55,
    )
    RoguePlanet = (
        "A planet-like object not bound to a star, floating in space",
        10,
        0.1,
    )
    OortCloud = (
        "A distant spherical shell of icy objects surrounding a star",
        10,
        0.05,
    )
    Comet = (
        "A small icy body that heats up and forms a tail when approaching a "
        "star",
        10,
        0.02,
    )

    def __init__(self, description, energy, gravitational_strength):
        self.description = description
        self.energy = energy  # Energy value between 10 and 100
        self.gravitational_strength = gravitational_strength  # Float
        # between 0 and 1

    def __str__(self):
        """Returns a human-readable description of the stellar object."""
        return self.name


if __name__ == "__main__":
    # Example usage
    stellar_object = StellarType.Pulsar
    print(
        stellar_object)  # Output: A rapidly spinning neutron star emitting
    # beams of electromagnetic radiation
    print(stellar_object.description)
    print(stellar_object.energy)  # Output: 70
    print(stellar_object.gravitational_strength)  # Output: 0.7

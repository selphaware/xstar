from enum import Enum


class StarType(Enum):
    Star = (
        "A luminous ball of gas, mostly hydrogen and helium, undergoing "
        "nuclear fusion",
        80,
        0.5,
        100
    )
    BlackHole = (
        "A region of spacetime with gravity so strong that nothing can "
        "escape it",
        10,
        1.0,
        3
    )
    NeutronStar = (
        "A compact stellar remnant of a massive star after a supernova",
        60,
        0.8,
        30
    )
    Pulsar = (
        "A rapidly spinning neutron star emitting beams of electromagnetic "
        "radiation",
        70,
        0.7,
        20
    )
    WhiteDwarf = (
        "A dense, cooling remnant of a low-mass star",
        40,
        0.3,
        150
    )
    RedGiant = (
        "A large, bright star in a late stage of stellar evolution",
        50,
        0.4,
        85
    )
    # Supernova = (
    #    "A powerful explosion marking the death of a massive star",
    #    100,
    #    0.6,
    # )
    Quasar = (
        "An extremely energetic active galactic nucleus powered by a "
        "supermassive black hole",
        100,
        0.9,
        1
    )
    Protostar = (
        "A young star in the early stage of formation",
        30,
        0.2,
        150
    )
    BrownDwarf = (
        "A substellar object not massive enough for nuclear fusion",
        20,
        0.15,
        500
    )
    Magnetar = (
        "A type of neutron star with an extremely powerful magnetic field",
        70,
        0.85,
        20
    )
    BinaryStar = (
        "A system of two stars orbiting a common center of mass",
        90,
        0.55,
        75
    )

    def __init__(self,
                 description,
                 energy,
                 gravitational_strength,
                 motion_decay):
        self.description = description
        self.energy = energy  # Energy value between 10 and 100
        self.gravitational_strength = gravitational_strength  # Float
        self.motion_decay = motion_decay

    def __str__(self):
        """Returns a human-readable description of the stellar object."""
        return self.name


if __name__ == "__main__":
    # Example usage
    stellar_object = StarType.Pulsar
    print(
        stellar_object)  # Output: A rapidly spinning neutron star emitting
    # beams of electromagnetic radiation
    print(stellar_object.description)
    print(stellar_object.energy)  # Output: 70
    print(stellar_object.gravitational_strength)  # Output: 0.7

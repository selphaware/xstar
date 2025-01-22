from enum import Enum


class PlanetType(Enum):
    Terrestrial = (
        "Rocky planet with a solid surface, often Earth-like", "Habitable",
        True)
    GasGiant = (
        "Large planet composed mostly of gases like hydrogen and helium",
        "Uninhabitable", False)
    IcePlanet = ("Planet covered in ice, often with sub-zero temperatures",
                 "Habitable with adaptation", False)
    DesertPlanet = ("Arid planet with minimal water and extreme temperatures",
                    "Partially Habitable", True)
    OceanPlanet = (
        "Planet covered entirely by water with little or no land", "Habitable",
        True)
    VolcanicPlanet = (
        "Planet with high volcanic activity and lava flows", "Uninhabitable",
        False)
    ArcticPlanet = (
        "Frozen planet with polar conditions and minimal vegetation",
        "Habitable with adaptation", False)
    JunglePlanet = (
        "Planet covered by dense forests and abundant vegetation", "Habitable",
        True)
    ToxicPlanet = (
        "Planet with a toxic atmosphere or surface, hostile to life",
        "Uninhabitable", False)
    RoguePlanet = (
        "Planet not bound to any star, drifting through space",
        "Uninhabitable",
        False)
    ArtificialPlanet = (
        "Planet created by advanced civilizations, e.g., Dyson Sphere",
        "Super Habitable", True)
    BarrenPlanet = (
        "Lifeless planet with no atmosphere or surface activity",
        "Uninhabitable",
        False)
    TidallyLockedPlanet = (
        "Planet with one side perpetually facing its star",
        "Partially Habitable",
        True)

    def __init__(self, description, habitability, supports_life):
        self.description = description
        self.habitability = habitability  # General assessment of habitability
        self.supports_life = supports_life  # Boolean indicating if it
        # naturally supports life

    def __str__(self):
        """Returns a human-readable description of the planet type."""
        return self.name


if __name__ == "__main__":
    # Example usage
    planet_type = PlanetType.Terrestrial
    print(
        planet_type)  # Output: Rocky planet with a solid surface,
    # often Earth-like
    print(planet_type.habitability)  # Output: Habitable
    print(planet_type.supports_life)  # Output: True

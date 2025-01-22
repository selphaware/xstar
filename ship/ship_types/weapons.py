from enum import Enum


class PrimaryWeapon(Enum):
    PhaserArray = ("Phaser array capable of precision targeting", 90, 1e6)
    DisruptorCannons = (
        "High-energy disruptor cannons for heavy damage", 85, 8e5)
    PlasmaBeams = ("Powerful plasma-based beam weaponry", 80, 7e5)
    QuantumTorpedoes = ("Advanced torpedoes with high energy yield", 95, 1e7)
    AntiprotonCannons = ("Devastating antiproton energy cannons", 100, 5e6)
    TachyonLances = ("Tachyon beam weapon with extreme precision", 88, 1.2e6)

    def __init__(self, description, power, range_km):
        self.description = description
        self.weapon_power = power
        self.weapon_range = range_km

    def __str__(self):
        """Returns a human-readable description of the weapon."""
        return self.description


class SecondaryWeapon(Enum):
    PhotonTorpedoes = (
        "Standard photon torpedoes for long-range combat", 75, 1e7)
    QuantumMines = ("Stationary mines with quantum-level detonation", 70, 5e5)
    PlasmaTorpedoes = ("Torpedoes with plasma-based warheads", 65, 8e6)
    PulseCannons = ("Rapid-fire cannons with medium power output", 60, 1e4)
    GravitonBeams = ("Focused graviton-based energy beam", 50, 2e5)
    PolaronBursts = ("Short-range polaron energy bursts", 55, 3e4)

    def __init__(self, description, power, range_km):
        self.description = description
        self.weapon_power = power
        self.weapon_range = range_km

    def __str__(self):
        """Returns a human-readable description of the weapon."""
        return self.description


if __name__ == "__main__":
    # Example usage
    secondary_weapon = SecondaryWeapon.PhotonTorpedoes
    print(
        secondary_weapon)  # Output: Standard photon torpedoes for
    # long-range combat
    print(secondary_weapon.weapon_power)  # Output: 75
    print(secondary_weapon.weapon_range)  # Output: 10000000.0

    # Example usage
    primary_weapon = PrimaryWeapon.PhaserArray
    print(
        primary_weapon)  # Output: Phaser array capable of precision targeting
    print(primary_weapon.weapon_power)  # Output: 90
    print(primary_weapon.weapon_range)  # Output: 1000000.0

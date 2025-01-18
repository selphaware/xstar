from enum import Enum


class Shields(Enum):
    Regenerative = ("Regenerative shields that self-repair over time", 800)
    Multiphasic = (
    "Shields tuned to multiple frequencies for enhanced protection", 900)
    Ablative = (
    "Shields that vaporize incoming energy to minimize damage", 700)
    Covariant = (
    "Highly durable shields capable of withstanding extreme impacts", 950)
    Deflector = ("Standard deflector shields for general-purpose defense", 600)
    Polarized = ("Polarized energy fields enhancing structural integrity", 500)
    Tachyon = (
    "Advanced shields utilizing tachyon fields for stealth defense", 850)
    Gravimetric = (
    "Shields designed to counteract gravitational distortions", 870)
    Temporal = (
    "Shields providing limited protection against temporal anomalies", 800)
    Quantum = (
    "High-energy shields tuned for defense against quantum-level attacks", 950)
    Biometric = (
    "Organic or hybrid shields responding to environmental threats", 650)
    EnergyDampening = (
    "Shields that absorb and dissipate energy from weapons fire", 700)

    def __init__(self, description, strength):
        self.description = description
        self.strength = strength

    def __str__(self):
        """Returns a human-readable description of the shield type."""
        return self.description


if __name__ == "__main__":
    # Example usage
    shield = Shields.Regenerative
    print(shield)  # Output: Regenerative shields that self-repair over time
    print(shield.strength)  # Output: 800

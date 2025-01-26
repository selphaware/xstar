from enum import Enum


class WarpEngine(Enum):
    StandardWarpDrive = ("Standard warp drive for general travel", 9.0, 7.0)
    AdvancedWarpCore = ("Highly efficient advanced warp core", 9.9, 9.5)
    QuantumSlipstream = ("Cutting-edge quantum slipstream drive", 9.99, 9.8)
    TranswarpDrive = ("Transwarp drive capable of extreme speeds", 10.5, 10.0)

    def __init__(self, description, maximum_warp, sustainable_warp):
        self.description = description
        self.maximum_warp = maximum_warp
        self.sustainable_warp = sustainable_warp

    def __str__(self):
        """Returns a human-readable description of the warp engine."""
        return self.description


class ImpulseEngine(Enum):
    FusionDrive = ("Standard fusion-powered impulse drive", 0.25)
    HighEfficiencyImpulse = ("High-efficiency impulse drive", 0.5)
    AdvancedIonDrive = ("Advanced ion-based impulse drive", 0.75)
    DilithiumPoweredDrive = ("Dilithium impulse drive", 1.0)
    ExperimentalImpulse = ("Experimental drive with extreme speeds", 2.0)

    def __init__(self, description, maximum_speed):
        self.description = description
        self.maximum_speed = maximum_speed

    def __str__(self):
        """Returns a human-readable description of the impulse engine."""
        return self.description


if __name__ == "__main__":
    # Example usage
    impulse_engine = ImpulseEngine.HighEfficiencyImpulse
    print(impulse_engine)  # Output: High-efficiency impulse drive
    print(impulse_engine.maximum_speed)  # Output: 0.5

    # Example usage
    warp_engine = WarpEngine.AdvancedWarpCore
    print(warp_engine)  # Output: Highly efficient advanced warp core
    print(warp_engine.maximum_warp)  # Output: 9.9
    print(warp_engine.sustainable_warp)  # Output: 9.5

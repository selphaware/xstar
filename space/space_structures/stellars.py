from stellar_types import StellarType


class StellarStructure(object):
    def __init__(
            self,
            name: str,
            stellar_type: StellarType,
            motion_decay: int  # number of turns it moves on its path
    ):
        self.name = name
        self.stellar_type: StellarType = stellar_type
        self.motion_decay: int = motion_decay

    @property
    def energy(self):
        return self.stellar_type.energy

    @property
    def stype(self):
        return self.stellar_type.name

    @property
    def gravitational_strength(self):
        return self.stellar_type.gravitational_strength

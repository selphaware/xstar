from stellar_types import StellarType


class StellarStructure(object):
    def __init__(
            self,
            name: str,
            stellar_type: StellarType,
    ):
        self.name = name
        self.stellar_type: StellarType = stellar_type

    @property
    def energy(self):
        return self.stellar_type.energy

    @property
    def stype(self):
        return self.stellar_type.name

    @property
    def gravitational_strength(self):
        return self.stellar_type.gravitational_strength

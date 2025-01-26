from space.space_structures.star_types import StarType
from xmath.structures import Z2_POS


class Star(object):
    def __init__(
            self,
            name: str,
            stellar_type: StarType,
    ):
        self.name = name + " Star"
        self.stellar_type: StarType = stellar_type

    @property
    def energy(self):
        return self.stellar_type.energy

    @property
    def instance_of(self):
        return self.stellar_type.name

    @property
    def gravitational_strength(self):
        return self.stellar_type.gravitational_strength

    @property
    def motion_decay(self):
        return self.stellar_type.motion_decay

    def print_info(self):
        print(f"Star Name: {self.name}")
        print(f"Star Type: {self.instance_of}")
        print(f"Energy: {self.energy}")
        print(f"Gravitational Strength: {self.gravitational_strength}")
        print(f"Motion Decay: {self.motion_decay}")

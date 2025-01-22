from space.space_structures.star_types import StarType


class Star(object):
    def __init__(
            self,
            name: str,
            stellar_type: StarType,
            motion_decay: int  # number of turns it moves on its path
    ):
        self.name = name
        self.stellar_type: StarType = stellar_type
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

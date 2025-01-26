from typing import List, Optional, Union
from math import ceil

from generic.factions import Faction
from ship.ship_types.engines import WarpEngine, ImpulseEngine
from ship.ship_types.missions import Mission
from ship.ship_types.shields import Shields
from ship.ship_types.weapons import PrimaryWeapon, SecondaryWeapon
from space.cosmic_structures.functions.calculate import calculate_magnitude
from xmath.structures import Z2_POS, R2_POS


class StarShip(object):
    def __init__(
            self,

            # basic
            name: str,
            faction: Faction,
            designation: str,
            captain: str,
            mission_type: Mission,
            operational_range: int,

            # defence
            shields: Shields,
            cloaking_device: bool,

            # weapons
            primary_weapons: List[PrimaryWeapon],
            secondary_weapons: List[SecondaryWeapon],

            # engines
            warp_engine: WarpEngine,
            impulse_engine: ImpulseEngine

            # sensors
            # TODO: SENDORS

    ):
        self.name: str = f"{name} ({designation})"
        self.faction: Faction = faction
        self.instance_of: str = f"STARSHIP: {faction}"  # TODO: StarShipType
        self.designation: str = designation
        self.captain: str = captain
        self.mission_type: Mission = mission_type

        self.operational_range: int = operational_range

        self.shields: Shields = shields
        self.shields_on: bool = False
        self.cloak_available: bool = cloaking_device
        self.cloaked: bool = False

        self.primary_weapons: List[PrimaryWeapon] = primary_weapons
        self.secondary_weapons: List[SecondaryWeapon] = secondary_weapons
        self.primary_target: Optional[Z2_POS] = None
        self.secondary_target: Optional[Z2_POS] = None

        self.warp_engine = warp_engine
        self.impulse_engine = impulse_engine
        self.warp_speed: float = 0.0
        self.impulse_speed: float = 0.0

        # motion
        self._course_vector: Z2_POS = (0, 0)

        # position
        self.position: Optional[Z2_POS] = None

        # TODO: Add sensors to get info on system

    def cloak(self, toggle: str) -> None:
        if self.cloak_available:
            toggle = toggle.upper()
            if toggle == "ON":
                self.cloaked = True
                self.shields_on = False

            elif toggle == "OFF":
                self.cloaked = False

            else:
                print("ERROR: cloak value should be ON or OFF.")

    def is_cloaked(self):
        return self.cloaked

    def set_impulse_speed(self, speed: float):
        self.impulse_speed = speed \
            if self.impulse_engine.maximum_speed > speed else \
            self.impulse_engine.maximum_speed

    @property
    def motion_vector(self) -> Union[Z2_POS, R2_POS]:
        required_vector: Z2_POS = self._course_vector

        sector_speed: float = self.impulse_speed * 10
        print("Sector Speed: ", sector_speed)

        required_sector_speed: float = calculate_magnitude(required_vector)

        motion_vector: Union[Z2_POS, R2_POS] = (0, 0)

        if required_sector_speed > 0:
            print("Req: ", required_sector_speed)

            factor: float = sector_speed / required_sector_speed

            isint: bool = isinstance(required_sector_speed, int)
            isfloat: bool = isinstance(required_sector_speed, float)

            motion_vector: Union[Z2_POS, R2_POS] = (
                required_vector[0] * factor if isfloat else ceil(
                    required_vector[0] * factor
                ),
                required_vector[1] * factor if isfloat else ceil(
                    required_vector[1] * factor
                ),
            )

        return motion_vector

    @property
    def course_vector(self) -> Union[Z2_POS, R2_POS]:
        return self._course_vector

    @course_vector.setter
    def course_vector(self, cv: Union[Z2_POS, R2_POS]):
        self._course_vector = cv

    # TODO: SENSORS

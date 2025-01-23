from typing import List, Optional

from generic.factions import Faction
from ship.ship_types.engines import WarpEngine, ImpulseEngine
from ship.ship_types.missions import Mission
from ship.ship_types.shields import Shields
from ship.ship_types.weapons import PrimaryWeapon, SecondaryWeapon
from xmath.structures import Z2_POS


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
            shields_version: int,

            # weapons
            primary_weapons: List[PrimaryWeapon],
            secondary_weapons: List[SecondaryWeapon],

            # engines
            warp_engine: WarpEngine,
            impulse_engine: ImpulseEngine

            # sensors
            # TODO: SENDORS

    ):
        self.name: str = name
        self.faction: Faction = faction
        self.instance_of: str = f"STARSHIP: {faction}"
        self.designation: str = designation
        self.captain: str = captain
        self.mission_type: Mission = mission_type

        self.operational_range: int = operational_range
        self.current_turnage: int = 0

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

        self.position: Z2_POS = (0, 0)

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

    def move(self, velocity: Z2_POS):
        pass

    # TODO: SENSORS

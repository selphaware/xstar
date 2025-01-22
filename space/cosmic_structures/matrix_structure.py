from typing import List

from space.cosmic_structures.system_sector import (SystemSector,
                                                   SECTOR_OBJECTS, \
                                                   SECTOR_OBJECT)
from xmath.structures import Z2_POS

VECTOR_SYSTEM_SECTOR = List[SystemSector]
MATRIX_SYSTEM_SECTOR = List[VECTOR_SYSTEM_SECTOR]


class SystemSectorMatrix(object):
    def __init__(self, size: Z2_POS):
        x_max, y_max = size

        self._sectors: MATRIX_SYSTEM_SECTOR = [
            [
                SystemSector(
                    # Empty Sector
                    f"SYSTEM Sector {i, j}",
                    (i, j),
                    None
                )
                for i in range(x_max)
            ]
            for j in range(y_max)
        ]

    @property
    def sectors(self):
        return self._sectors

    def set_sector(self, position: Z2_POS, system_sector: SystemSector):
        x, y = position
        self._sectors[x][y] = system_sector

    def set_sector_name(self, position: Z2_POS, name: str):
        x, y = position
        self._sectors[x][y].name = name

    def set_sector_objects(self, position: Z2_POS, objects: SECTOR_OBJECTS):
        x, y = position
        self._sectors[x][y].objects = objects

    def add_sector_object(self, position: Z2_POS, obj: SECTOR_OBJECT):
        x, y = position
        self._sectors[x][y].objects.append(obj)

    def get_sector(self, position: Z2_POS) -> SystemSector:
        x, y = position
        return self._sectors[x][y]

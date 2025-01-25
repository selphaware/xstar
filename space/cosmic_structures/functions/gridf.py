from typing import Union

from space.cosmic_structures.matrix_structure import SystemSectorMatrix
from space.space_structures.planet import Planet
from space.space_structures.stars import Star
from xmath.structures import Z2_POS


def initialise_grid(grid_size: Z2_POS) -> SystemSectorMatrix:
    grid: SystemSectorMatrix = SystemSectorMatrix(grid_size)

    return grid


def add_object_to_grid(
        grid: SystemSectorMatrix,
        pos: Z2_POS,
        name: str,
        obj: Union[Star, Planet]
) -> None:
    grid.set_sector_name(pos, name)
    grid.add_sector_object(pos, obj)

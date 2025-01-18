from typing import Tuple

R2 = Tuple[int, int]

from typing import List, Optional, Union

VECTOR = List[GridCell]
MATRIX = List[VECTOR]


class Grid(object):
    def __init__(self, size: R2):
        x_max, y_max = size

        self.cells: MATRIX = [
            [
                GridCell(position=(i, j))
                for i in range(x_max)
            ]
            for j in range(y_max)
        ]

    def get_cell(self, position: R2):
        x, y = position
        return self.cells[x][y]
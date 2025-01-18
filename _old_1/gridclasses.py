from objclasses import GridCell, R2
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


class DGrid(object):
    def __init__(self, size: R2, position: R2 = (0, 0)):
        self.position = position
        self.size: R2 = size
        x_max, y_max = size
        self.x_max, self.y_max = size

        self.level: int = x_max * y_max

        self.__DMATRIX = List[List[DGrid]]
        DMATRIX = self.__DMATRIX

        self.__DMatrixType = Optional[DMATRIX]
        DMatrixType = self.__DMatrixType

        self.grid: Grid = Grid(size=(x_max, y_max))

        if x_max + y_max > 2:
            self.dmatrix: DMatrixType = [
                [
                    DGrid(
                        size=(
                            x_max - (i + 1),
                            y_max - (j + 1)
                        ),
                        position=(i, j)
                    )
                    for i in range(x_max)
                ]
                for j in range(y_max)
            ]

        else:
            self.dmatrix: DMatrixType = None

    def get_dgrid(self, position: R2, depth: int = 0):
        x, y = position
        if depth == 0:
            return self.dmatrix[x][y]
        else:
            pass


# TODO: CREATE WORMHOLE
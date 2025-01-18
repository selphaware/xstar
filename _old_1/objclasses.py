import random
from typing import List, Tuple

R2 = Tuple[int, int]

NAMES = [chr(65 + i) for i in range(26)]


class CellObject(object):
    def __init__(self, id: int):
        self.id: int = id
        self.name: str = random.choice(NAMES) + " - " + str(id)


class GridCell(object):
    def __init__(self, position: R2):
        self.position = position
        self.cell_objects: List[CellObject] = [
            CellObject(i)
            for i in range(random.randint(0, 5))
        ]

import hashlib
import random
from typing import Optional, List
from datetime import datetime
from time import time


def random_int_generator(
        a: int,
        b: int,
        seed: str,
        unique: bool = False
):
    idx = 0

    visited = []

    while True:
        # seed code (unique on each yield iteration)

        seed_str = seed + (
                str(datetime.now())
                + str(time())
                + (str(idx + 1) * (idx + 1))
        )

        random.seed(seed_str)

        rnd_int = random.randint(a, b)

        if (not unique) or (rnd_int not in visited):
            yield rnd_int

        visited.append(rnd_int)

        idx += 1


if __name__ == "__main__":
    print("\n\n")
    rgen = random_int_generator(0, 1000)
    for i in range(10):
        print(next(rgen))

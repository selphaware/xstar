import hashlib
import random
from typing import Optional, List
from datetime import datetime
from time import time


def random_int_generator(a: int, b: int):
    idx = 0

    while True:
        # seed code (unique on each yield iteration)
        seed_str = (
                str(datetime.now())
                + str(time())
                + (str(idx + 1) * (idx + 1))
        )

        random.seed(seed_str)

        yield random.randint(a, b)

        idx += 1


if __name__ == "__main__":
    print("\n\n")
    rgen = random_int_generator(0, 1000)
    for i in range(10):
        print(next(rgen))

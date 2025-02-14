import numpy as np
from numpy import atan2
from typing import List, Tuple
from math import degrees, pi


def perpendicular(a):
    a = normalize(a)
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def normalize(a):
    a = np.array(a)
    return a / np.linalg.norm(a)


def unit_vector(vector):
    return vector / np.linalg.norm(vector)


def angle_between_vectors(
        v1: List[float],
        v2: List[float],
        degree: bool = False,
        use_atan2: bool = True
) -> float:
    if use_atan2:
        angle = atan2(v2[1], v2[0]) - atan2(v1[1], v1[0])

    else:
        v1 = np.array(v1)
        v2 = np.array(v2)
        dotv = np.dot(v1, v2)
        denom_v1 = np.sqrt(np.dot(v1, v1))
        denom_v2 = np.sqrt(np.dot(v2, v2))
        angle = np.arccos(dotv / (denom_v1 * denom_v2))

    if angle > pi:
        angle = -1 * (2 * pi - angle)
    elif angle < -pi:
        angle = -1 * (-2 * pi + angle)

    if degree:
        return degrees(angle)

    else:
        return angle

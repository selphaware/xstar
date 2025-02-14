import numpy as np
from numpy import atan2
from typing import List, Tuple
from math import degrees, pi


def rotation_matrix(in_vector: np.array, theta: float) -> np.array:
    # Rotation matrix in 2D
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s],
                  [s, c]])

    # Apply rotation (multiply matrix R with vector shifted)
    rotated = (R @ in_vector.T).T

    return rotated


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
        _v1: List[float],
        _v2: List[float],
        degree: bool = False,
        use_atan2: bool = True,
        normalize: bool = False
) -> float:
    v1 = unit_vector(np.array(_v1))
    v2 = unit_vector(np.array(_v2))

    if use_atan2:
        angle = atan2(v2[1], v2[0]) - atan2(v1[1], v1[0])

    else:
        v1 = np.array(v1)
        v2 = np.array(v2)
        dotv = np.dot(v1, v2)
        denom_v1 = np.sqrt(np.dot(v1, v1))
        denom_v2 = np.sqrt(np.dot(v2, v2))
        angle = np.arccos(dotv / (denom_v1 * denom_v2))

    angle = angle % (np.sign(angle) * 2 * pi)

    if normalize:
        if angle < -pi:
            angle = angle % pi
        elif angle > pi:
            angle = angle % -pi

    if degree:
        return degrees(angle)

    else:
        return angle

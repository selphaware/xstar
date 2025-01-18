import numpy as np

from xmath.structures import EQN_STRUCT

PARAMETRIC_EQNS: EQN_STRUCT = {

    "log_spiral": [
        lambda t, C, L: C * np.exp(L * t) * np.cos(t),
        lambda t, C, L: C * np.exp(L * t) * np.sin(t)
    ],

    "circle": [
        lambda t, r: r * np.cos(t),
        lambda t, r: r * np.sin(t)
    ],

    "asteroid_curve": [
        lambda t, C: C * (np.cos(t) ** 3),
        lambda t, C: C * (np.sin(t) ** 3)
    ]

}

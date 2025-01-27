import numpy as np

from xmath.structures import EQN_STRUCT

PARAMETRIC_EQNS: EQN_STRUCT = {

    "log_spiral": [  # used for galaxy deployment of systems
        lambda t, C, L: C * np.exp(L * t) * np.cos(t),
        lambda t, C, L: C * np.exp(L * t) * np.sin(t)
    ],

    "log_spiral2": [  # used for galaxy deployment of systems
        lambda t, C, L, rot, hs, vs: C * np.exp(L * t) * np.cos(rot * t) + hs,
        lambda t, C, L, rot, hs, vs: C * np.exp(L * t) * np.sin(rot * t) + vs
    ],

    "circle": [  # used for planetary system planet/objects/ships deployment
        lambda t, r: r * np.cos(t),
        lambda t, r: r * np.sin(t)
    ],

    "elipse": [
        lambda t, a, hs, vs: a * np.cos(t) + hs,
        lambda t, b, hs, vs: b * np.sin(t) + vs
    ],

    "asteroid_curve": [
        lambda t, C: C * (np.cos(t) ** 3),
        lambda t, C: C * (np.sin(t) ** 3)
    ],

    "epitrochoid": [
        lambda t, c, n: np.cos(t) - c * np.cos(n * t),
        lambda t, c, n: np.sin(t) - c * np.sin(n * t)
    ],

    "lemniscate_bernoulli": [
        lambda t: np.cos(t) / (1 + np.sin(t) ** 2),
        lambda t: (np.sin(t) * np.cos(t)) / (1 + np.sin(t) ** 2)
    ]

}

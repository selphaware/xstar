import numpy as np

from xmath.structures import EQN_STRUCT

PARAMETRIC_EQNS: EQN_STRUCT = {

    "log_spiral": [  # used for galaxy deployment of systems
        lambda t, C, L, h_shift, _: C * np.exp(L * t) * np.cos(t) + h_shift,
        lambda t, C, L, _, v_shift: C * np.exp(L * t) * np.sin(t) + v_shift
    ],

    "circle": [  # used for planetary system planet/objects/ships deployment
        lambda t, r, h_shift, _: r * np.cos(t) + h_shift,
        lambda t, r, _, v_shift: r * np.sin(t) + v_shift
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

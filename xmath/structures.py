from typing import Tuple, List, Dict, Any, Union

Lambda = Any
EQN_STRUCT = Dict[str, List[Lambda]]

Z2_POS = Tuple[int, int]
R2_POS = Tuple[float, float]

Z1 = List[int]
Z2 = List[Z2_POS]
Z2_MATRIX = List[Z1]

R1 = List[float]
R2 = List[R2_POS]

UNIVERSE_STRUCT = Dict[                     # universe
            str,                            # galaxy keys
            Dict[                           # galaxy
                str,                        # galaxy name
                Union[
                    str,                    # galaxy name
                    R2,                     # galaxy motion path
                    Dict[                   # star system
                        str,                # star system name
                        Dict[
                            str,            # star system keys
                            Union[
                                str,        # star system name
                                R2,         # origin
                                List[R2]    # all planet orbit paths
                            ]
                        ]
                    ]
                ]
            ]
        ]

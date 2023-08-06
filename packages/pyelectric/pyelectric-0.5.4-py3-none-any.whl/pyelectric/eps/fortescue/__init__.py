import cmath
import math
from typing import Tuple

import numpy as np

from . import transformer


def compose(Va0: complex, Va1: complex, Va2: complex) -> Tuple[complex, complex, complex]:
    symmetric = np.array([Va0, Va1, Va2])

    a = cmath.rect(1, math.radians(120))
    T = np.array([
        [1, 1, 1],
        [1, a**2, a],
        [1, a, a**2],
    ])

    V_real = np.dot(T, symmetric)
    Va, Vb, Vc = V_real[0], V_real[1], V_real[2]
    return Va, Vb, Vc


def decompose(Va: complex, Vb: complex, Vc: complex) -> Tuple[complex, complex, complex]:
    symmetric = np.array([Va, Vb, Vc])

    a = cmath.rect(1, math.radians(120))
    T = np.array([
        [1, 1, 1],
        [1, a, a**2],
        [1, a**2, a],
    ])

    V_real = np.dot(T, symmetric)/3
    Va0, Va1, Va2 = V_real[0], V_real[1], V_real[2]
    return Va0, Va1, Va2

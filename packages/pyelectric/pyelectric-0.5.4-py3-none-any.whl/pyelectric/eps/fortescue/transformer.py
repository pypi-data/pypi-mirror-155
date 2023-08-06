import math
from typing import Tuple

from pyelectric.ac.phasor import Phasor


def solve_phase_y_delta(Ia: complex, Ib: complex) -> Tuple[complex, complex, complex]:
    Ia_phasor, Ib_phasor = Phasor(Ia), Phasor(Ib)
    Ia_phasor.phase += math.radians(-30)
    Ib_phasor.phase += math.radians(+30)
    Ia, Ib, = Ia_phasor.value, Ib_phasor.value
    return Ia, Ib

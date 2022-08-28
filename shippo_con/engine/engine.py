import numpy as np

from collections import namedtuple

from shippo_con.engine.engine_params import EngineParams

Status = namedtuple('Status', ['raw_input', 'g1', 'g2', 'params'])

class Engine:

    def __init__(self, params: EngineParams = None) -> None:
        self.params = params or EngineParams()
        self.reset()

    def reset(self):
        self._raw_input = np.zeros(2, dtype=np.float64)
        self._g1 = np.zeros(2, dtype=np.float64)
        self._g2 = np.zeros(2, dtype=np.float64)

    def update(self, _input):
        self._raw_input = _input
        self._g1 *= 0.99
        self._g1 += self._raw_input
        self._g2 += self._g1
        self._g2 *= 0.09
        self._params = np.tanh(0.005 * self._g2)

    def get_status(self):
        return Status(
            self._raw_input,
            self._g1,
            self._g2,
            self._params,
        )

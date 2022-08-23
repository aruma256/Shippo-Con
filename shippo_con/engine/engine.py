import numpy as np

from shippo_con.engine.engine_params import EngineParams

class Engine:

    def __init__(self, params:EngineParams=None) -> None:
        self.params = params or EngineParams()
        self.reset()

    def reset(self):
        self._raw_pos = np.zeros(2, dtype=np.float64)
        self._xy_abs_max = np.ones(2, dtype=np.float64)

    def update(self, velocity):
        self._raw_pos *= self.params.decay_factor
        self._raw_pos += velocity
        np.maximum(self._xy_abs_max, np.abs(self._raw_pos), out=self._xy_abs_max)

    def calc_pos(self):
        return self._raw_pos / self._xy_abs_max


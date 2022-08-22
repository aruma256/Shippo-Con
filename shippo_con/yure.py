import numpy as np

DECAY_RATE = 0.99

class Yure:

    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self._raw_pos = np.zeros(2, dtype=np.float64)
        self._xy_abs_max = np.ones(2, dtype=np.float64)

    def update(self, gyro):
        self._raw_pos *= DECAY_RATE
        self._raw_pos += gyro
        np.maximum(self._xy_abs_max, np.abs(self._raw_pos), out=self._xy_abs_max)

    def calc_pos(self):
        return self._raw_pos / self._xy_abs_max



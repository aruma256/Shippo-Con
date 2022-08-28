import numpy as np


class EngineParams:

    def __init__(self, decay_factor=0.99):
        self.decay_factor = decay_factor
        self.g2_decay_factor = 0.09
        self.amp = np.array([50, 70])

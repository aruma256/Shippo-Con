import numpy as np
from pyjoycon import JoyCon, get_L_id

class JoyconInput:

    def __init__(self) -> None:
        self._joycon = JoyCon(*get_L_id())

    def get(self):
        return np.array([self._joycon.get_gyro_x(), self._joycon.get_gyro_y()], dtype=np.float64)

    def is_reset_button_pressed(self):
        return self._joycon.get_button_l_stick()

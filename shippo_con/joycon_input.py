import numpy as np
from pyjoycon import JoyCon, get_L_id, get_R_id


class JoyconInput:

    def __init__(self, side) -> None:
        if side == 'R':
            self._joycon = JoyCon(*get_R_id())
        else:
            self._joycon = JoyCon(*get_L_id())

    def get(self):
        gyro = [self._joycon.get_gyro_x(), self._joycon.get_gyro_y()]
        return np.array(gyro, dtype=np.float64)

    def is_reset_button_pressed(self):
        return self._joycon.get_button_l_stick()

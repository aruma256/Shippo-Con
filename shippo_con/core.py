from time import sleep
from pythonosc import udp_client
from shippo_con.engine.engine import Engine
from shippo_con.joycon_input import JoyconInput

FPS = 72


class Core:

    def __init__(self) -> None:
        self._input = JoyconInput()
        self._engine = Engine()
        self._client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

    def run(self):
        try:
            self._mainloop()
        except KeyboardInterrupt:
            pass

    def _mainloop(self):
        while True:
            sleep(1/FPS)

            if self._input.is_reset_button_pressed():
                self._engine.reset()
                continue

            self._engine.update(self._input.get())
            pos = self._engine.calc_pos()

            self._client.send_message("/avatar/parameters/Fx_Tail_X", pos[0])
            self._client.send_message("/avatar/parameters/Fx_Tail_Y", pos[1])

from time import sleep
from pythonosc import udp_client
from shippo_con.engine.engine import Engine
from shippo_con import gui
from shippo_con.engine.engine_params import EngineParams
from shippo_con.joycon_input import JoyconInput

FPS = 72
NAME = 'Shippo-Con'
VERSION = '0.1.0'


class Core:

    def __init__(self, server, port, param_x_name, param_y_name) -> None:
        self._input = None
        self.engine_params = EngineParams()
        self._engine = Engine(self.engine_params)
        self._client = udp_client.SimpleUDPClient(server, port)
        self._running = True
        self.param_x_name = param_x_name
        self.param_y_name = param_y_name

    def connect_joycon(self, side):
        self._input = JoyconInput(side)

    def run(self):
        self._gui = gui.GUI(self)
        self._gui.create()
        try:
            self._mainloop()
        except KeyboardInterrupt:
            pass

    def _mainloop(self):
        while self._running:
            sleep(1/FPS)

            if not self._input:
                continue

            if self._input.is_reset_button_pressed():
                self._engine.reset()
                continue

            self._engine.update(self._input.get())

            status = self._engine.get_status()
            self._gui.update(status)

            self._client.send_message(self.param_x_name, status.params[0])
            self._client.send_message(self.param_y_name, status.params[1])

    def kill(self):
        self._running = False

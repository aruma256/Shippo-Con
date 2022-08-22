from pythonosc import udp_client
from time import sleep

from shippo_con.joycon_input import JoyconInput
from shippo_con.yure import Yure

client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

FPS = 72

input_ = JoyconInput()
yure = Yure()

try:
    while True:
        sleep(1/FPS)

        if input_.is_reset_button_pressed():
            yure.reset()
            continue

        yure.update(input_.get())
        pos = yure.calc_pos()

        client.send_message("/avatar/parameters/Fx_Tail_X", pos[0])
        client.send_message("/avatar/parameters/Fx_Tail_Y", pos[1])

except KeyboardInterrupt:
    pass



import json
from shippo_con.core import Core

with open('config.json') as f:
    config = json.load(f)

core = Core(
    config['OSC']['server'],
    config['OSC']['port'],
    config['OSC']['param_x_name'],
    config['OSC']['param_y_name'],
)
core.run()

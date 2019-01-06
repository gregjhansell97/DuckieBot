from duckie_bot.cameras import WebCamera
from duckie_bot.cars import RPiCar, DebugCar
from duckie_bot.servers import duckie_server
from duckie_bot import modes

#arg parse

def debug_modes():
    debug_car = DebugCar()
    web_camera = WebCamera()
    duckie_server.run(
        car=debug_car, 
        camera=web_camera,
        mode_modules=modes.__all__
    )

def run_modes():
    pass


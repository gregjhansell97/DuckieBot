from duckie_bot.cars.car import Car

class DebugCar(Car):

    def __init__(self):
        Car.__init__(self)

    def refresh_motor_speed(self, speed, omega):
        print("speed: " + str(speed) + "\tomega: " + str(omega))

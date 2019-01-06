try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
except ImportError:
    pass

import time
import atexit

from duckie_bot.cars.car import Car

#unicycle model
class RPiCar(Car):
    '''
    Controls the speed of the car based on desired tangential and rotational speed.
    Motors are ramped rather than stepping between speeds

    Attributes:
        speed_ratio
    '''
    def __init__(self, speed_ratio):
        Car.__init__(self)

        self.speed_ratio = speed_ratio

        self._calibration = {}
        self._calibration["offset_left"] = 0.2
        self._calibration["gain_left"] = 1
        self._calibration["offset_right"] = 0.2
        self._calibration["gain_right"] = 1

        self._mh = Adafruit_MotorHAT(addr=0x60)
        atexit.register(self._turn_off_motors)

        self._left_motor = self._mh.getMotor(1)
        self._right_motor = self._mh.getMotor(2)

    def _turn_off_motors(self):
        self._left_motor.run(Adafruit_MotorHAT.RELEASE)
        self._right_motor.run(Adafruit_MotorHAT.RELEASE)

    def refresh_motor_speed(self, speed, omega):
        speed_left = (speed *self.speed_ratio - omega *(1-self.speed_ratio))
        speed_right = (speed *self.speed_ratio + omega *(1-self.speed_ratio))

        if speed_left > 0:
            speed_left = self._calibration["offset_left"] + speed_left*(1-self._calibration["offset_left"])
            self._left_motor.setSpeed(int(speed_left*255))
            self._left_motor.run(Adafruit_MotorHAT.FORWARD)
        elif speed_left == 0:
            self._left_motor.setSpeed(0)
        else: # speed_left < 0
            speed_left = self._calibration["offset_left"] - speed_left*(1-self._calibration["offset_left"])
            self._left_motor.setSpeed(int(speed_left*255))
            self._left_motor.run(Adafruit_MotorHAT.BACKWARD)

        if speed_right > 0:
            speed_right = self._calibration["offset_right"] + speed_right*(1-self._calibration["offset_right"])
            self._right_motor.setSpeed(int(speed_right*255))
            self._right_motor.run(Adafruit_MotorHAT.FORWARD)
        elif speed_right == 0:
            self._right_motor.setSpeed(0)
        else: # speed_right < 0
            speed_right = self._calibration["offset_right"] - speed_right*(1-self._calibration["offset_right"])
            self._right_motor.setSpeed(int(speed_right*255))
            self._right_motor.run(Adafruit_MotorHAT.BACKWARD)

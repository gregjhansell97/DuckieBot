'''
runs the PWM code to drive the motors, and get input for a desired tangential and rotational speed
'''

'''
Import Adafruit_MotorHAT for driving the motors
'''
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit


class Unicycle:
    '''
    Controls the speed of the car based on desired tangential and rotational speed.
    Motors are ramped rather than stepping between speeds

    Attributes:
        _speed(float): Current tangential speed
        _omega(float): Current rotational speed
        _motor_accal(float): Motor acceleration used in the ramp in _set_motor_speed
        _calibration(dict): Motor calibration values
    '''


    def __init__(self, speed_ratio=0.7, speed=0, omega=0):

        '''
        delete this constructor when you're done with it alex,
        keep variables lower case and under score dO nOT uSeD cAmeL cAsE

        Args:
            motor_accle(float):
            speed(float):
            omega(float):
        '''

        self._speed = speed
        self._omega = omega
        self._speed_ratio = speed_ratio

        self._calibration = {}
        self._calibration["offset_left"] = 0.2
        self._calibration["gain_left"] = 1
        self._calibration["offset_right"] = 0.2
        self._calibration["gain_right"] = 1

        self._mh = Adafruit_MotorHAT(addr=0x60)
        atexit.register(self._turnOffMotors)

        self._left_motor = self._mh.getMotor(1)
        self._right_motor = self._mh.getMotor(2)

    def set_omega(self, omega):
        '''
        Set rotational speed

        Args:
            omega(float): Rotational speed between -1 and 1. 0 is no turning, >0 is turning left
        '''
        self._omega = omega
        self._set_motor_speed()
        ''' input (range?)'''

        pass

    def set_speed(self, speed):
        '''
        Set car speed

        Args:
            speed(float): Tangential speed between -1 and 1. 0 is no tangential speed, >0 is forward
        '''

        self._speed = speed
        self._set_motor_speed()
        ''' input (range?)'''

        pass

    def _turnOffMotors(self):
        self._left_motor.run(Adafruit_MotorHAT.RELEASE)
        self._right_motor.run(Adafruit_MotorHAT.RELEASE)

    

    def _set_motor_speed(self):

        '''
        Ramps the motor speeds based on calibration values and maximum acceleration
        '''
        
        speed_left = (self._speed *self._speed_ratio - self._omega *(1-self._speed_ratio))
        speed_right = (self._speed *self._speed_ratio + self._omega *(1-self._speed_ratio))
        

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
if __name__ == "__main__":
    u = Unicycle()
    u.set_speed(1)
    time.sleep(1000)
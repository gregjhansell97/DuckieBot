'''
control.py runs the PWM code to drive the motors, and get input for a desired tangential and rotational speed

'''
class Control:
    '''
    Controls the speed of the car based on desired tangential and rotational speed.
    Motors are ramped rather than stepping between speeds 

    Attributes:
        _speed(float): Current tangential speed
        _omega(float): Current rotational speed
        _motor_accal(float): Motor acceleration used in the ramp in _set_motor_speed
        _calibration(dict): Motor calibration values
    '''


    def __init__(self,  motor_accel=0, speed=0, omega=0):
        '''
        <description>: delete this constructor when you're done with it alex,
        keep variables lower case and under score dO nOT uSeD cAmeL cAsE

        Args:
            motor_accle(float):
            speed(float):
            omega(float):
        '''
        self._speed = speed
        self._omega = omega
        self._motor_accel = motor_accel

        self._calibration = {}
        self._calibration["offset_left"] = 0
        self._calibration["gain_left"] = 1
        self._calibration["offset_right"] = 0
        self._calibration["gain_right"] = 1
        
        pass
    
    def set_omega(self, omega):
        '''
        <description>: Set rotational speed

        Args:
            omega(float): Rotational speed between -1 and 1. 0 is no turning, >0 is turning left
        '''
        pass

     def set_speed(self, speed):
        '''
        <description>: Set car speed

        Args:
            speed(float): Tangential speed between -1 and 1. 0 is no tangential speed, >0 is forward 
        '''
        pass

    def _set_motor_speed(self, speed_left, speed_right):
        '''
        <description>: Ramps the motor speeds based on calibration values and maximum acceleration

        Args:
            speed_left(float): Speed of the left motor, between -1 and 1. 0 is off, >1 is forward
            speed_right(float): Speed of the right motor, between -1 and 1. 0 is off, >1 is forward
        '''
        pass
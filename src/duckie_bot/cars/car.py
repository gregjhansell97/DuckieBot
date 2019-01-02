class Car:
    '''
    Controls the speed of the car based on desired tangential and rotational speed.

    Attributes:
        speed(float): Current tangential speed
        omega(float): Current rotational speed
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

        self.speed = speed
        self.omega = omega

    def set_omega(self, omega):
        '''
        Set rotational speed

        Args:
            omega(float): Rotational speed between -1 and 1. 0 is no turning, >0 is turning left
        '''
        if omega < -1: omega = -1
        if omega > 1: omega = 1
        self.omega = omega
        self.refresh_motor_speed(self.speed, self.omega)

    def set_speed(self, speed):
        '''
        Set car speed

        Args:
            speed(float): Tangential speed between -1 and 1. 0 is no tangential speed, >0 is forward
        '''
        if speed < -1: speed = -1
        if speed > 1: speed = 1
        self.speed = speed
        self.refresh_motor_speed(self.speed, self.omega)

    def refresh_motor_speed(self, speed, omega):
        '''
        '''
        pass


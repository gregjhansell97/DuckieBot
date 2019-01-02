class Unicycle:
    def __init__(self,  motor_accel=0, speed=0, omega=0):
        self._speed = speed
        self._omega = omega
        self._motor_accel = motor_accel

        self._calibration = {}
        self._calibration["offset_left"] = 0
        self._calibration["gain_left"] = 1
        self._calibration["offset_right"] = 0
        self._calibration["gain_right"] = 1
    def set_omega(self, omega):
        print('Omega set to {:f}'.format(omega))
    def set_speed(self, speed):
        print('speed set to {:f}'.format(speed))

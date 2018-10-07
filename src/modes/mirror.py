#external modules
from collections import namedtuple
import cv2

#local modules
from modes.mode import AbstractMode

class Mirror(AbstractMode):
    '''
    '''
    def __init__(self, car=None):
        '''
        '''
        AbstractMode.__init__(self)

        #forces applied to speeds
        Forces = namedtuple("Forces", ["applied", "drag"])
        self.speed_forces = Forces(applied=0.3, drag=0.2)
        self.omega_forces = Forces(applied=0.3, drag=0.2)

        #speeds themselves
        self.speed = 0
        self.omega = 0

        #abstraction to hardware
        self.car = car

    def drag(self, speed, drag):
        if speed < -drag:
            speed += drag
        elif speed < 0:
            speed = 0
        if speed > drag:
            speed -= drag
        elif speed > 0:
            speed = 0
        #puts a cap limit on max speed
        if abs(speed - 0) < 0.0001:
            speed = 0
        if speed < 0:
            return max(speed, -1)
        else:
            return min(speed, 1)

    def tick(self):
        '''
        '''
        #starting values (to be compared later)
        start_speed = self.speed
        start_omega = self.omega

        if "W" in self.keys_pressed:#up
            self.speed += self.speed_forces.applied
        if "S" in self.keys_pressed:#down
            self.speed -= self.speed_forces.applied
        if "A" in self.keys_pressed:#left
            # print("Mirror turn left")
            self.omega -= self.omega_forces.applied
        if "D" in self.keys_pressed:#right
            # print("Mirror turn right")
            self.omega += self.omega_forces.applied
        self.speed = self.drag(self.speed, self.speed_forces.drag)
        self.omega = self.drag(self.omega, self.omega_forces.drag)
        #deaccelerates items

        #reflect changes in car
        if start_speed != self.speed:
            self.car.set_speed(self.speed)
        if start_omega != self.omega:
            self.car.set_omega(self.omega)

    def frame(self, frame):
        '''
        '''
        frame = cv2.flip( frame, 1 )
        return frame

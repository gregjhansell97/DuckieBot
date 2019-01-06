#external modules
from collections import namedtuple
import cv2, os, random
from pathlib import Path

#local modules
from duckie_bot.modes.mode import Mode

class Squid(Mode):
    '''
    '''
    def __init__(self, camera=None, car=None):
        '''
        '''
        Mode.__init__(self, camera=camera, car=car)

        #forces applied to speeds
        Forces = namedtuple("Forces", ["applied", "drag"])
        self.speed_forces = Forces(applied=0.3, drag=0.2)
        self.omega_forces = Forces(applied=0.3, drag=0.2)

        #speeds themselves
        self.speed = 0
        self.omega = 0

        #self.imgpath = random.choice([x for x in os.listdir("gui/static/ink_img")
        #       if os.path.isfile(os.path.join("gui/static/ink_img", x))])

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

    def tick(self, keys_pressed):
        '''
        '''
        #starting values (to be compared later)
        start_speed = self.speed
        start_omega = self.omega

        if "W" in keys_pressed:#up
            self.speed += self.speed_forces.applied
        if "S" in keys_pressed:#down
            self.speed -= self.speed_forces.applied
        if "A" in keys_pressed:#left
            self.omega += self.omega_forces.applied
        if "D" in keys_pressed:#right
            self.omega -= self.omega_forces.applied
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
        # background = frame
        # self.imgpath='ink9.png'
        # print(self.imgpath)
        # overlay = cv2.imread('gui/static/ink_img/'+self.imgpath)
        # overlay = cv2.resize(overlay, (background.shape[1], background.shape[0]))
        # background = cv2.imread('gui/static/ink_img/ink8.png')
        # background = cv2.flip( background, 1 )
        # cv2.imshow('image',background)

        # print(os.getcwd())
        # print (Path('.'))
        # added_image = cv2.addWeighted(background,0.7,overlay,0.3,0)

        return frame

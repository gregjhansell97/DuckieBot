from collections import namedtuple
from threading import Thread, Event
import signal
import sys

class Driver:
    '''
    '''
    def __init__(self, car=None):
        '''
        '''
        #list of keys currently being held down
        self._keys_pressed = set()
        
        #forces applied to speeds
        Forces = namedtuple("Forces", ["applied", "drag"])
        self.speed_forces = Forces(applied=0.3, drag=0.3)
        self.omega_forces = Forces(applied=0.3, drag=0.3)
        
        #speeds themselves
        self.speed = 0
        self.omega = 0

        #abstraction to hardware
        self.car = car
        
        #thread that runs the motor
        self.thread = None
    
    def _tick(self):
        '''
        '''
        #starting values (to be compared later)
        start_speed = self.speed
        start_omega = self.omega

        #deaccelerates items
        self.speed += self.speed_forces.drag*(self.speed < 0)
        self.speed -= self.speed_forces.drag*(self.speed > 0)
        self.omega += self.omega_forces.drag*(self.omega < 0)
        self.omega -= self.omega_forces.drag*(self.omega > 0)
        
        if "w" in self._keys_pressed:#up
            self.speed += self.speed_forces.applied
        if "s" in self._keys_pressed:#down
            self.speed -= self.speed_forces.applied
        if "a" in self._keys_pressed:#left
            self.omega += self.omega_forces.applied
        if "d" in self._keys_pressed:#right
            self.omega -= self.omega_forces.applied
        
        #cuts the limit to their maximum 
        if self.speed > 1:
            self.speed = 1
        elif self.speed < -1:
            self.speed = -1
        if self.omega > 1:
            self.speed = 1
        elif self.speed < -1:
            self.speed = -1  
        
        #reflect changes in car
        if start_speed != self.speed:
            self.car.set_speed(self.speed)
        if start_omega != self.omega:
            self.car.set_omega(self.omega)
            
    def start(self):
        '''
        '''
        class ControlThread(Thread):
            def __init__(self, tick=None):
                Thread.__init__(self)
                self.stop_flag = Event() 
                self.tick = tick
                signal.signal(signal.SIGINT, self._on_exit)
            def stop(self):
                self.stop_flag.set()
            def _on_exit(self, *args):
                self.stop()
                sys.exit()
            def run(self):
                while not self.stop_flag.wait(0.3):
                    self.tick()
        self.thread = ControlThread(tick=self._tick)
        self.thread.start()

    def stop(self):
        '''
        '''
        if self.thread is not None:
            self.thread.stop()
        self.thread = None

    def set_input(key, pressed):
        '''
        '''
        if pressed: #pressed
            self._keys_pressed.add(key)
        else: #released
            self._keys_pressed.discard(key)

    def frame(self, frame):
        '''
        '''
        return frame
        

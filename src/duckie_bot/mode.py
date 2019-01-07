#external modules
from abc import ABC, abstractmethod
import signal
import sys
from threading import Thread, Event

class _ControlThread(Thread):
    '''
    subclass of thread used in Mode class
    '''
    def __init__(self, mode=None):
        '''
        mode(Mode): the mode to loop through and call tick
        '''
        Thread.__init__(self)
        self.stop_flag = Event()
        self.mode = mode
    def stop(self):
        self.stop_flag.set()
    def _on_exit(self, *args):
        self.stop()
        sys.exit()
    def run(self):
        while not self.stop_flag.wait(0.3):
            if self.mode is None: continue
            self.mode.tick()

class Mode(ABC):
    '''
    abstract base class for all modes

    Attributes:
        camera(duckie_rodeo.Camera): camera feed
        keys_pressed(set): a set of keys currently being pressed
        car(duckie_rode.cars.Car): car provided to the mode to drive with

    Static Private Attributes: "we're all adults here" - daemon the koala
        _thread(_ControlThread): single thread running the mode provided to it
    '''

    _thread = None

    def _set_input(self, key, pressed):
        '''
        recieved update on keys pressed and modifies self.keys_pressed
        accordingly

        Args:
            key(str): the key that is currently being pressed or depressed
            pressed(bool): whether the key is pressed or depressed
        '''
        if pressed:
            self.keys_pressed.add(key)
        else: #key is depressed
            self.keys_pressed.discard(key)

    def start(self, camera=None, car=None):
        '''
        starts a mode by spinning up a thread, stops any other mode threads
        currently active; leaving as public so user could override camera and
        car settings passed into it; should still call this instance of start
        in their implementation

        Args:
            camera(duckie_bot.Camera): camera feed
            car(duckie_bot.Car): car that controls duckie_bot
        '''
        self.keys_pressed = set()
        self.camera = camera
        self.car = car
        if Mode._thread is None:
            Mode._thread = _ControlThread(mode=self)
            Mode._thread.start()
        Mode._thread.mode = self
        self.camera.mode = self

    @abstractmethod
    def frame(self, frame):
        '''
        modifies a frame

        Args:
            frame(Frame): current frame from camera feed

        Returns:
            (Frame): modified frame for website camera feed
        '''
        pass

    @abstractmethod
    def tick(self):
        '''
        when thread is currently active tick method is called on loop passing in
        keys pressed
        '''
        pass

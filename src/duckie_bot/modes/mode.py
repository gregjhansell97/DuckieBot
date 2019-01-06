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
            self.mode.tick(self.mode._keys_pressed)

class Mode(ABC):
    '''
    abstract base class for all modes

    Attributes:
        _initialized(bool): checks if __init__ was called
        _keys_pressed(set): a set of keys currently being pressed
        camera(duckie_rodeo.cameras.Camera): camera feed
        car(duckie_rode.cars.Car): car provided to the mode to drive with

    Static Attributes:
        _thread(_ControlThread): single thread running the mode provided to it
    '''

    _thread = None

    def __init__(self, camera=None, car=None):
        '''
        Args:
            camera(duckie_rodeo.cameras.Camera): camera feed
            car(duckie_rode.cars.Car): car provided to the mode to drive with
        '''
        self._initialized = True
        self._keys_pressed = set()
        self.camera = camera
        self.car = car

    def _check_initialization(self):
        '''
        verifies that the base class's constructor was invoked

        Raises:
           Mode Constructor Uninitialized
        '''
        if not "_initialized" in self.__dict__:
            raise(Exception("Mode Constructor Uninitialized"))

    def _set_input(self, key, pressed):
        '''
        recieved update on keys pressed and modifies self._keys_pressed
        accordingly

        Raises:
            Mode Constructor Uninitialized
        '''
        self._check_initialization()
        if pressed:
            self._keys_pressed.add(key)
        else: #key is depressed
            self._keys_pressed.discard(key)

    def _process_frame(self):
        '''
        uses the camera to return video feed; camera frame may be modified by
        the active mode

        Returns:
            generator(bytes): yields image data over to the requestor
        '''
        return self.camera.process_frame()

    def start(self):
        '''
        starts a mode by spinning up a thread, stops any other mode threads
        currently active

        Raises:
            Mode Constructor Uninitialized
        '''
        self._check_initialization()
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
    def tick(self, keys_pressed):
        '''
        when thread is currently active tick method is called on loop passing in
        keys pressed

        Args:
            keys_pressed(set): a set of keys currently being pressed
        '''
        pass

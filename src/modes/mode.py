#external modules
from abc import ABC, abstractmethod
import signal
import sys
from threading import Thread, Event

'''
'''
class AbstractMode(ABC):
    '''
    '''
    def __init__(self):
        '''
        '''
        self.thread = None
        self.initialized = True
        #list of keys currently being held down
        self.keys_pressed = set()

    def start(self):
        '''
        '''
        if not "initialized" in self.__dict__:
            raise(Exception("AbstractMode Constructor Uninitialized"))
        if self.thread is not None:
            return
        class ControlThread(Thread):
            def __init__(self, tick=None):
                Thread.__init__(self)
                self.stop_flag = Event()
                self._tick = tick
                signal.signal(signal.SIGINT, self._on_exit)
            def stop(self):
                self.stop_flag.set()
            def _on_exit(self, *args):
                self.stop()
                sys.exit()
            def run(self):
                while not self.stop_flag.wait(0.3):
                    self._tick()
        self.thread = ControlThread(tick=self.tick)
        self.thread.start()

    def stop(self):
        '''
        '''
        if not "initialize" in self.__dict__:
            raise(Exception("AbstractMode Constructor Uninitialized"))
        if self.thread is not None:
            self.thread.stop()
        self.thread = None

    def set_input(self, key, pressed):
        '''
        '''
        if pressed.lower() == "true": #pressed
            self.keys_pressed.add(key)
        else: #released
            self.keys_pressed.discard(key)

    @abstractmethod
    def frame(self, frame):
        '''
        '''
        pass
    @abstractmethod
    def tick(self):
        '''
        '''
        pass

#external modules
from abc import ABC, abstractmethod

class Camera(ABC):
    '''
    represents a streamable camera like one on a raspberry-pi or a web cam

    Attributes:
        framerate(int): number of frames per second
        mode(duckie_bot.Mode): the active mode
        resolution((int, int)): quality/size of each frame
    '''
    def __init__(self, mode=None):
        '''
        constructor that should be invoked in child class

        Args:
            mode(duckie_bot.Mode): the active mode
        '''
        self.mode = mode

    @abstractmethod
    def process_frame(self):
        '''
        creates a frame, passes it to the active mode to process and returns a
        generator to create more frames; frame has to be a jpg

        Yields:
            (bytes): frame jpg data
        '''
        pass

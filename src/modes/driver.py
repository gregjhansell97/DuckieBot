#from Controls import ControlDebug
from picamera import PiCamera
import cv2


class Driver:
    '''
    '''
    def __init__(self):
        self._keys_pressed = []
        self._keys_released = []

        self.camera = PiCamera()
        self.camera.resolution(REPLACE, REPLACE)
        self.camera.framerate = FRAME_RATE


    def set_input(next_pressed=[], next_released=[]):
        pass

    def frame(self, frame):
        return frame

    def _modify_frame(self, frame):
        pass        
        

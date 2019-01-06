import cv2

from duckie_bot.cameras.camera import Camera

class WebCamera(Camera):
    '''
    '''
    def __init__(self, framerate=32, resolution=(640, 480), mode=None):
        Camera.__init__(self)
        self.framerate = framerate
        self.resolution = resolution
        self.raw_capture = cv2.VideoCapture(0)
        self.mode = mode

    def process_frame(self):
        '''
        '''
        #check for blank mode
        while True:
            ret, frame = self.raw_capture.read()
            frame = self.mode.frame(frame)
            ret, jpg = cv2.imencode('.jpg', frame)
            yield (b'--jpgboundary\r\n'+
                b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')

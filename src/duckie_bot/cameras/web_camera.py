#external modules
import cv2

#inhouse
from duckie_bot.cameras.camera import Camera

class WebCamera(Camera):
    '''
    Camera instance for web-cams

    Attributes:
        raw_capture(cv2.RawCapture): raw video frame with cv2 camera
    '''
    def __init__(self, mode=None):
        Camera.__init__(
            self,
            mode=mode
        )
        self.raw_capture = cv2.VideoCapture(0)

    def process_frame(self):
        while True:
            ret, frame = self.raw_capture.read()
            if self.mode is not None:
                frame = self.mode.frame(frame)
            ret, jpg = cv2.imencode('.jpg', frame)
            yield (b"--jpgboundary\r\nContent-Type: image/jpeg\r\n\r\n" +
                   jpg.tostring() +
                   b'\r\n')

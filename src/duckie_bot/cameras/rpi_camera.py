from duckie_bot.cameras.camera import AbstractCamera
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    pass
import time

class RPiCamera(AbstractCamera):
    '''
    '''
    def __init__(self, framerate=32, resolution=(640, 480)):
        AbstractCamera.__init__(self)
        self.framerate = framerate
        self.resolution = resolution
        self.camera = None
        self.rawCapture = None
        self.stop_feed = False

    def restart(self):
        '''
        '''
        if self.camera != None: #camera is active
            self.stop_feed = True
            time.sleep(0.2) #give time for camera to end feed
            camera.close()
            self.stop_feed = False

        #initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera(framerate=self.framerate, resolution=self.resolution)
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)

        #allow the camera time to warm up
        time.sleep(0.1)

    def process_frame(self, mode):
        '''
        '''
        self.restart()

        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            if self.stop_feed:
                break
            
            image =  mode.frame(frame.array)
            ret, jpg = cv2.imencode(".jpg", image)
            yield (b'--jpgboundary\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')
            #clear the stream in preparation for next frame
            rawCapture.truncate(0)

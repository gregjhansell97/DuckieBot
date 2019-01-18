from duckie_bot.cameras.camera import Camera
import cv2
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    pass
import time

class RPiCamera(Camera):
    '''
    represents a streamable camera like one on a raspberry-pi or a web cam

    Attributes:
        framerate(int): number of frames per second
        resolution((int, int)): quality/size of each frame
        self.camera(PiCamera): the camera on the raspberry pi
        self.raw_capture(PiRGBArray): raw frame data from the camera
        self.stop_feed(bool): ends the camera feed when set to true
    '''
    def __init__(self, framerate=32, mode=None, resolution=(640, 480)):
        '''
        Args:
            framerate(int): number of frames per second
            mode(duckie_bot.Mode): the active mode
            resolution((int, int)): quality/size of each frame
        '''
        Camera.__init__(self, mode=mode)
        self.framerate = framerate
        self.resolution = resolution
        self.camera = None
        self.raw_capture = None
        self.stop_feed = False

    def _restart(self):
        '''
        resets the camera and raw_capture ensuring to stop the camera feed
        before starting another one (may no longer be a problem). There is
        atleast a 0.1 second pause
        '''
        # TODO this method may no longer be needed
        if self.camera != None: #camera is active
            self.stop_feed = True
            time.sleep(0.2) #give time for camera to end feed
            self.camera.close()
            self.stop_feed = False

        #initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera(framerate=self.framerate, resolution=self.resolution)
        self.raw_capture = PiRGBArray(self.camera, size=self.resolution)

        #allow the camera time to warm up
        time.sleep(0.1)

    def process_frame(self):
        self._restart()

        for frame in self.camera.capture_continuous(
            self.raw_capture,
            format="bgr",
            use_video_port=True
        ):
            if self.stop_feed: break
            processed_frame =  self.mode.frame(frame.array)
            ret, jpg = cv2.imencode(".jpg", processed_frame)
            yield (b"--jpgboundary\r\nContent-Type: image/jpeg\r\n\r\n" +
                   jpg.tostring() +
                   b'\r\n')
            #clear the stream in preparation for next frame
            self.raw_capture.truncate(0)
#
#
# def process_frame():
#     '''
#     Function to process camera frames continuously and send them to the app
#     '''
#     global camera
#     global stop_feed
#     if camera != None:
#         stop_feed = True
#         time.sleep(0.2)
#         camera.close()
#         stop_feed = False
#
#     # initialize the camera and grab a reference to the raw camera capture
#     camera = PiCamera(framerate=32, resolution=(640, 480))
#     rawCapture = PiRGBArray(camera, size=(640, 480))
#
#     # allow the camera to warmup
#     time.sleep(0.1)
#
#     # capture frames from the camera
#     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#         if stop_feed:
#             break
#         # grab the raw NumPy array representing the image, then initialize the timestamp
#         # and occupied/unoccupied text
#         image = mode.frame(frame.array)
#         # show the frame
#         ret, jpg = cv2.imencode('.jpg', image)
#         yield (b'--jpgboundary\r\n'+
#             b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')
#         # clear the stream in preparation for the next frame
#         rawCapture.truncate(0)

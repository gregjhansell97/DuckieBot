from duckie_bot.cameras.camera import Camera
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    pass
import time

class RPiCamera(Camera):
    '''
    '''
    def __init__(self, framerate=32, resolution=(640, 480)):
        Camera.__init__(self)
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

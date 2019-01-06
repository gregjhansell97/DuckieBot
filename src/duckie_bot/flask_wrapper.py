#external modules
import cv2
from flask import Flask, render_template, request, Response
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

#local modules
import modes
from controls import Unicycle

stop_feed = False
camera = None

#globals "eyes roll but such is flask" -daemon the koala
car = Unicycle()
mode_modules = {m.__name__: m(car) for m in modes.__all__}
app = Flask(
    "__main__",
    static_folder="./gui/static",
    template_folder="./gui/templates")
mode = mode_modules["Driver"]
mode.start()

@app.route('/', methods=['GET'])
def index():
    '''
    Routes for index, serves main page

    Returns:
        Template: view of index.html
    '''
    mode_names=list(mode_modules.keys())
    print(mode_names)
    return render_template('index.html',modes=mode_names)

@app.route('/key_action', methods=['POST'])
def key_action():
    '''
    '''
    global mode
    if request.method == 'POST':
        key = request.form['key']
        pressed = request.form['action']
        mode.set_input(key, pressed)
    return '';

@app.route('/change_mode', methods=['POST'])
def change_mode():
    '''
    '''
    global mode
    global mode_modules
    if request.method == 'POST':
        mode_name = request.form['mode']
        print("mode:", mode_name)
        mode.stop()
        mode = mode_modules[mode_name]
        mode.start()
        print("mode: ",mode_name)
    return '';

def process_frame():
    '''
    Function to process camera frames continuously and send them to the app
    '''
    global camera
    global stop_feed
    if camera != None:
        stop_feed = True
        time.sleep(0.2)
        camera.close()
        stop_feed = False
    
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera(framerate=32, resolution=(640, 480))
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if stop_feed:
            break
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = mode.frame(frame.array)
        # show the frame
        ret, jpg = cv2.imencode('.jpg', image)
        yield (b'--jpgboundary\r\n'+
            b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
@app.route('/video_feed')
def video_feed():
    '''
    Route for video feed

    Returns:
        Response: response to front end after calling process_frame function.
    '''
    return Response(process_frame(),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

class Server:
    '''
    '''
    def __init__(self, host="0.0.0.0", port=9694, **kwargs):
        '''
        '''
        self.host = host
        self.port = port
    def run(self):
        '''
        '''
        app.run(host=self.host, port=self.port)
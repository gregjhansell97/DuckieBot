#!/usr/bin/env python
from modes import Driver
from controls import DebugControl
from flask import Flask, render_template, request, Response
import cv2
from opencvutils import Camera
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ModuleNotFoundError:
    pass
import time

app = Flask(__name__)
car = DebugControl()
driver = Driver(car)

@app.route('/', methods=['GET'])
def index():
    '''
    Routes for index, serves main page
   
    Returns: 
        Template: view of index.html
    '''    
    modes=["Driver","LineFollower","DrunkDriver","Mirror"]
    return render_template('index.html',modes=modes)

@app.route('/key_action', methods=['POST'])
def key_action():
    if request.method == 'POST':
        key = request.form['key']
        pressed = request.form['action']
        # driver.set_input(key, pressed)
        print('key: ',key)
    return '';

@app.route('/change_mode', methods=['POST'])
def change_mode():
    if request.method == 'POST':
        mode = request.form['mode']
        print("mode: ",mode)
    return '';
        
def process_frame():
    '''
    Function to process camera frames continuously and send them to the app
    '''
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera(framerate=32, resolution=(640, 480))
    rawCapture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = driver.frame(frame).array
        # show the frame
        ret, jpg = cv2.imencode('.jpg', image)
        yield (b'--jpgboundary\r\n'+
            b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

def process_frame_pc():
    cap = cv2.VideoCapture(0)
    print ("capture:", cap)
    while True:
        ret, frame = cap.read()
        ret, jpg = cv2.imencode('.jpg', frame)
        yield (b'--jpgboundary\r\n'+
            b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    '''
    Route for video feed
    
    Returns: 
        Response: response to front end after calling process_frame function.
    '''
    return Response(process_frame(),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')


if __name__ == "__main__":
     app.run(host='0.0.0.0')

#external modules
import cv2
from flask import Flask, render_template, request, Response

#local modules
from modes import Driver
from stubbed.controls import Unicycle

#globals "eyes roll but such is flask" -daemon the koala
app = Flask(
    "__main__",
    static_folder="./gui/static",
    template_folder="./gui/templates")
car = Unicycle()
mode = Driver(car)
mode.start()

@app.route('/', methods=['GET'])
def index():
    modes=["Driver","LineFollower","DrunkDriver","Mirror"]
    return render_template('index.html',modes=modes)

@app.route('/key_action', methods=['POST'])
def key_action():
    if request.method == 'POST':
        key = request.form['key']
        pressed = request.form['action']
        mode.set_input(key, pressed)
    return '';

@app.route('/change_mode', methods=['POST'])
def change_mode():
    if request.method == 'POST':
        mode = request.form['mode']
        print("mode: ",mode)
    return '';

def process_frame():
    cap = cv2.VideoCapture(0)
    print ("capture:", cap)
    while True:
        ret, frame = cap.read()
        frame = mode.frame(frame)
        ret, jpg = cv2.imencode('.jpg', frame)
        yield (b'--jpgboundary\r\n'+
            b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(process_frame(),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

class Server:
    def __init__(self, host="0.0.0.0", port=9694, **kwargs):
        self.host = host
        self.port = port
    def run(self):
        app.run(host=self.host, port=self.port)

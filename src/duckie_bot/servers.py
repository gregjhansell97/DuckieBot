#external modules
import os
from flask import Flask, render_template, request, Response

#local modules
import duckie_bot.modes



path = os.path.dirname(os.path.realpath(__file__))
app = Flask(
    "__main__",
    static_folder=path + "/gui/static",
    template_folder=path + "/gui/templates")

class DuckieServer:
    '''
    a loose singleton that runs the Flask app as well as keeps track of the list of modes, camera and current mode
    
    Attributes:
        camera (duckie_rodeo.cameras.AbstractCamera): camera feed
        modes (dict): key is the name of the mode, value is an instance of the mode class
    '''
    def __init__(self):
        self.camera = None
        self.modes = []
        self.mode = None

    def _set_mode(self, mode):
        #TODO add some error handling here
        if self.mode is mode: #no change needed
            return
        elif self.mode is None:
            self.mode = mode
        else:
            self.mode.stop()
            self.mode = mode
        self.camera.mode = mode
        self.mode.start()

    def get_mode_names(self):
        return list(self.modes.keys())

    def change_mode(self, mode_name):
        self._set_mode(self.modes[mode_name])

    def key_action(self, key, pressed):
        self.mode.set_input(key, pressed)

    def process_frame(self):
        return self.camera.process_frame()

    def run(
        self, 
        host="0.0.0.0", 
        port=9694, 
        car=None, 
        camera=None,
        mode_modules=[]):
        '''
        '''
        
        self.camera = camera
        self.modes = {m.__name__: m(car) for m in mode_modules}
        self._set_mode(next(iter(self.modes.values())))

        app.run(host=host, port=port)

duckie_server = DuckieServer()

@app.route('/', methods=['GET'])
def index():
    '''
    Routes for index, serves main page

    Returns:
        Template: view of index.html
    '''
    return render_template('index.html',modes=duckie_server.get_mode_names())

@app.route('/key_action', methods=['POST'])
def key_action():
    '''
    '''
    if request.method == 'POST':
        key = request.form['key']
        pressed = request.form['action']
        duckie_server.key_action(key, pressed)
    return '';

@app.route('/change_mode', methods=['POST'])
def change_mode():
    '''
    '''
    if request.method == 'POST':
        mode_name = request.form['mode']
        duckie_server.change_mode(mode_name)
    return '';

@app.route('/video_feed')
def video_feed():
    '''
    Route for video feed

    Returns:
        Response: response to front end after calling process_frame function.
    '''
    return Response(duckie_server.process_frame(),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')


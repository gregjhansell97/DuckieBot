#external modules
import os
from flask import Flask, render_template, request, Response

#local modules
import duckie_bot.modes

class DuckieServer(Flask):
    '''
    used to generate a singleton instance below that uses modes, camera, and car
    passed in to generate a website that controls the car based on different
    modes; the singleton instance needs to invoke the method run in order to
    start the server; most state variables are none until this happens

    Attributes:
        camera(duckie_rodeo.cameras.Camera): camera feed
        modes(dict): instances of the modes key off of class name
        _mode(duckie_rodeo.Mode): the _set_mode method is needed to set the mode
           never write to this state variable directly
    '''
    def __init__(self):
        # calls super constructor
        path = os.path.dirname(os.path.realpath(__file__))
        Flask.__init__(
            self,
            "__main__",
            static_folder=path + "/gui/static",
            template_folder=path + "/gui/templates")
        # state variables initially empty
        self.camera = None
        self.modes = []
        self._mode = None

    def _set_mode(self, mode):
        '''
        changes the mode field variable

        Args:
            mode(duckie_rodeo.Mode): the mode to be changed to
        '''
        #TODO add some error handling here
        if self._mode is mode: #no change needed
            return
        elif self._mode is None:
            self._mode = mode
        else:
            self._mode.stop()
            self._mode = mode
        self.camera.mode = mode
        self._mode.start()

    def get_mode_names(self):
        '''
        Returns:
            list of class names of the available modes
        '''
        return list(self.modes.keys())

    def change_mode(self, mode_name):
        '''
        changes the active mode given a mode_name

        Args:
            mode_name(str): the name of the mode class
        '''
        self._set_mode(self.modes[mode_name])

    def key_action(self, key, pressed):
        '''
        invoked when key is pressed down or unpressed

        Args:
            key(str): the character on the keyboard
            pressed(bool): key pressed or depressed
        '''
        self._mode.set_input(key, pressed)

    def process_frame(self):
        '''
        uses the camera to return video feed; camera frame may be modified by
        the active mode

        Returns:
            generator(bytes): yields image data over to the requestor
        '''
        return self.camera.process_frame()

    def run(
        self,
        host="0.0.0.0",
        port=9694,
        car=None,
        camera=None,
        mode_modules=[]):
        '''
        starts the server; blocking call

        Args:
            host(str): host name (usually an ip address)
            port(int): the port number to access
            car(duckie_rode.cars.Car): car provided to the mode to drive with
            camera(duckie_rodeo.cameras.Camera): camera feed
            modes(dict): instances of the modes key off of class name
        '''
        self.camera = camera
        self.modes = {m.__name__: m(car) for m in mode_modules}
        self._set_mode(next(iter(self.modes.values())))

        Flask.run(self, host=host, port=port)

duckie_server = DuckieServer()


@duckie_server.route('/', methods=['GET'])
def index():
    '''
    routes for index; provides modes available; serves main page

    Returns:
        (Template): view of index.html
    '''
    return render_template('index.html',modes=duckie_server.get_mode_names())

@duckie_server.route('/key_action', methods=['POST'])
def key_action():
    '''
    listens for post commands regarding keys pressed and depressed

    Returns:
        (str): an empty string
    '''
    if request.method == 'POST':
        key = request.form['key']
        pressed = request.form['action']
        duckie_server.key_action(key, pressed.lower() == "true")
    return '';

@duckie_server.route('/change_mode', methods=['POST'])
def change_mode():
    '''
    listens for post command regarding a change in modes described as a string

    Returns:
        (str): an empty string
    '''
    if request.method == 'POST':
        mode_name = request.form['mode']
        duckie_server.change_mode(mode_name)
    return '';

@duckie_server.route('/video_feed')
def video_feed():
    '''
    route for video feed

    Returns:
        (Response): response of a frame to front end after getting the generator
            from the process_frame function
    '''
    return Response(
        duckie_server.process_frame(),
        mimetype='multipart/x-mixed-replace; boundary=--jpgboundary'
    )

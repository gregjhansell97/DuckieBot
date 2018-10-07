#!/usr/bin/env python
from modes import Driver
'''
1. bring randy's flask here and run it from main
2. modify to use picamera
3. import Driver and pass to frame
'''
from flask import Flask, render_template, Response
import cv2
from picamera import PiCamera
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def process_frame():
	driver = Driver()

	self.camera = PiCamera()
    self.camera.resolution = (640, 480)
    self.camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    	# show the frame
		cv2.imshow("Frame", image)
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		frame = driver.frame(frame)
		
		ret, jpg = cv2.imencode('.jpg', frame)
		yield (b'--jpgboundary\r\n'+
			b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(process_frame(),
			mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')


if __name__ == "__main__":
    app.run(host='0.0.0.0')

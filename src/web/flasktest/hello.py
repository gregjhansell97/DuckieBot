#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
from opencvutils import Camera
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')


def gen():
	cap = cv2.VideoCapture(0)
	print ("capture:", cap)
	while True:
		ret, frame = cap.read()
		ret, jpg = cv2.imencode('.jpg', frame)
		yield (b'--jpgboundary\r\n'+
			b'Content-Type: image/jpeg\r\n\r\n' + jpg.tostring() + b'\r\n')


@app.route('/video_feed')
def video_feed():
	return Response(gen(),
			mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

if __name__ == '__main__':
	app.run(host='0.0.0.0')
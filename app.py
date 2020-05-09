#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, send_from_directory
import threading
import cv2
from camera_opencv import Camera
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
camera = Camera()

FPS = 1

@app.route('/')
def index():
	return render_template('home.html')

@socketio.on('connect')
def connect():
	emit('after connect',  {'data':'connected to server'})

@app.route('/saved/<path:filepath>')
def saved(filepath):
	return send_from_directory('saved', filepath)

def updateCamera():
	threading.Timer(1.0/FPS, updateCamera).start()
	frame = camera.get_frame()
	socketio.emit('imageUpdate', {'image_data':frame})

updateCamera()

if __name__ == '__main__':
	socketio.run(app, debug=False, log_output=False, host='0.0.0.0')

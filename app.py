#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, send_from_directory
from camera_opencv import Camera
from flask_socketio import SocketIO
from flask_socketio import send, emit
import os
import threading
import cv2
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
camera = Camera()

FPS = 1

@app.route('/')
def index():
	return render_template('home.html')

@socketio.on('connect')
def connect():
	files = getListOfFiles()
	emit('after connect',  {'files':files})

@app.route('/saved/<path:filepath>')
def saved(filepath):
	return send_from_directory('saved', filepath)

def getListOfFiles():
	dirName = os.getcwd() + '/saved/'
	listOfFile = os.listdir(dirName)
	allFiles = list()

	for entry in listOfFile:
		allFiles.append(entry)

	try:
		allFiles.remove('.gitkeep')
	except:
		print('something went wrong with removing .gitkeep')

	try:
		allFiles.remove('.DS_Store')
	except:
		print('something went wrong with removing .DS_Store')

	            
	return allFiles

def updateCamera():
	initTime = time.time() * 1000
	frame = camera.get_frame()
	delay = time.time()*1000 - initTime
	socketio.emit('imageUpdate', {'image_data':frame, 'delay':delay})
	threading.Timer(1.0/FPS+(delay/1000), updateCamera).start()

updateCamera()

if __name__ == '__main__':
	socketio.run(app, debug=False, log_output=False, host='0.0.0.0')

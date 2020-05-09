import os
import cv2
import time
import datetime
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    savedImagePath = os.getcwd() + '/saved/'
    font = cv2.FONT_HERSHEY_SIMPLEX
    latestFile = ''

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @classmethod
    def frames(self):
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        while True:
            # read current frame
            try:
                _, img = camera.read()

                img = cv2.resize(img, (256, 144))

                imgName = str(round(time.time()*10))

                self.latestFile = imgName

                currentDT = datetime.datetime.now()

                cv2.putText(img,currentDT.strftime("%Y-%m-%d %H:%M:%S"),(10,20), Camera.font, 0.5,(0,0,0),2)

                # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                # Detect the faces
                # faces = face_cascade.detectMultiScale(gray, 1.4, 4)
                # Draw the rectangle around each face
                # for (x, y, w, h) in faces:
                #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

                status = cv2.imwrite(Camera.savedImagePath + imgName + '.jpg', img)

                # encode as a jpeg image and return it
                yield cv2.imencode('.jpg', img)[1].tostring()
            except:
                print('something went wrong')

            
from flask import Flask
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import cv2
import base64
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

model = YOLO('yoga_pose_classifier_v4/weights/best.pt')
results = model('Goddess-Pose-for-Pose-Page-e1574893769111.jpeg', conf=0.5, save=False, show=True)

# @socketio.on("send_image")
# def generate_frames(message):
# 	results = model('Goddess-Pose-for-Pose-Page-e1574893769111.jpeg', conf=0.5, save=False, show=False)
# 	emit("send_conf", str(results[0].keypoints))

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)

from flask import Flask
from datetime import date
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import cv2
import base64
import time
import numpy as np
from beat_detection import simple
import database
from PIL import Image
from io import BytesIO
import os
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()

weights_path = os.path.join(os.getcwd(), "yoga_pose_classifier_v4", "weights", "best.pt")
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=1e8)


DB = {
    "host": os.getenv("host"),
    "database": os.getenv("dbname"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "port": os.getenv("port"),
    "sslmode":"require"
}

db = database.DBConnector()

if os.getenv("is_local") == "True":
    db.create_database_if_not_exists(DB['database'], DB['user'], DB['password'], DB['port'])
    
db.connect()

model = YOLO('yoga_pose_classifier_v4/weights/best.pt')


@socketio.on("login")
def login(message):
    id = db.login(message['username'], message['password'])
    emit("logged-in", id)

@socketio.on("register")
def register(message):
    id = db.signup(message['username'], message['password'])
    emit("registered", id)

@socketio.on("add_points")
def add_points(message):
    print(message)
    db.add_points(message['id'], message['add'])

@socketio.on("get_logs")
def add_points(message):
    print('here')
    logs = db.get_daily_logs_by_user(message['id'])
    for log in logs:
        log["log_date"] = log["log_date"].strftime("%Y-%m-%d")

    emit('send_logs', logs)

@socketio.on("get_user_info")
def add_points(message):
    print('here')
    logs = db.get_user_info(message['id'])
    print(logs)

    emit('send_user', logs)

@socketio.on("get_earned")
def get_earned(message):
    query = " b"
    db.add_points(message['id'], message['add'])

@socketio.on("request_beats")
def request_beats(message):
    # print(message['path'])
    emit("send_beats", simple.get_beats(message['path']).tolist())

@socketio.on("send_image")
def classify_pose(message):
    #results is a list of Result objects
	img_pil = Image.open(BytesIO(message['message'])).convert("RGB")
	img_np = np.array(img_pil)
	results = model(img_np,verbose=False,show=False) #repress print, showing


	if len(results) == 0 or len(results[0].boxes) == 0:
		emit("send_results", [0, 4])

	#extract classes
	classes_dict = results[0].names #dictionary following idx:class_name
	#extract class prediction for bounding box
	predicted_classes = results[0].boxes.cls.cpu().numpy() #convert tensor to numpy
	confidence_scores = results[0].boxes.conf.cpu().numpy()
	#get only the highest prediction: forces 1-person detection at a time
	#u can change this
	max_idx = np.argmax(confidence_scores)
	highest_class_idx = int(predicted_classes[max_idx])
	highest_conf = float(confidence_scores[max_idx])
	highest_class_name = classes_dict[highest_class_idx]

	print(highest_class_idx, highest_class_name)

	emit("send_results", [float(highest_conf), highest_class_idx])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)

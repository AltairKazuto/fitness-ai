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

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=1e8)

DB_CONFIG = {
    "host": "localhost",
    "database": "workout_tracker1",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}
DB_CONFIG['host'] = 'localhost' 
DB_CONFIG['user'] = 'postgres'
DB_CONFIG['password'] = 'postgres'
DB_CONFIG['port'] = 5432
DB_CONFIG['database'] = 'workout_tracker1'

db = database.DBConnector()
db.create_database_if_not_exists(DB_CONFIG['database'], DB_CONFIG['user'], DB_CONFIG['password'], DB_CONFIG['port'])

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
    print('b')
    db.add_points(message['id'], message['add'])

@socketio.on("get_logs")
def add_points(message):
    print('here')
    logs = db.get_daily_logs_by_user(message['id'])
    for log in logs:
        log["log_date"] = log["log_date"].strftime("%Y-%m-%d")

    emit('send_logs', logs)

@socketio.on("get_earned")
def get_earned(message):
    query = " b"
    db.add_points(message['id'], message['add'])

@socketio.on("request_beats")
def request_beats(message):
    # print(message['path'])
    emit("send_beats", simple.get_beats(message['path']).tolist())

# def generate_frames(message):
	# img_pil = Image.open(BytesIO(message['message'])).convert("RGB")
	# img_np = np.array(img_pil)
# 	results = model(img_np, conf=0.5, save=False, show=False)
# 	emit("send_results", str(results[0].keypoints))

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
    # if db.connect():
    #     db.init_db() # initialize database if new app

    #     print(db.signup("macncheese2", "passpass"))
    #     the_user = db.login("macncheese2", "passpass")
    #     db.add_points(the_user, 230)
        
    #     db.close()
    socketio.run(app, host="0.0.0.0", port=5000)

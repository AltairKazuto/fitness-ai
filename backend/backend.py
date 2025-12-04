from flask import Flask
from flask_socketio import SocketIO, emit
from ultralytics import YOLO
import cv2
import base64
import time
import numpy as np
from beat_detection import simple
from PIL import Image
from io import BytesIO
import os

weights_path = os.path.join(os.getcwd(), "yoga_pose_classifier_v4", "weights", "best.pt")
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=1e8)

model = YOLO(weights_path)

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
    socketio.run(app, host="0.0.0.0", port=5000)

# Welcome to BEAT IT!

**Beat It** is an application in which users can do fun and engaging exercise activities at the comfort of their homes for free. This is a project for _CS 176 (2025-2026 1st Semester)_

**Contributors:**

- Gabor, Ryv
- Resano, Gabrielle
- Rodriguez, Shaira

# Prerequisites

- **npm (Node.js)**
- **Python 3.x**
- **(Optional) PostgreSQL**

  Verify using:

```
npm --version
python --version
psql --version
```

# Installation Guide

Clone the repo to your local machine

```
git clone https://github.com/AltairKazuto/fitness-ai.git
cd fitness-ai
```

To install the required dependencies needed for the project, either run the installation script or manually install.

#### Installation Script

##### Windows

```
// fitness-ai/
install.bat
```

##### Unix (Linux/Mac)

```
// fitness-ai/
chmod +x install.sh
./install.sh
```

#### Manual Install

```
// fitness-ai/frontend
npm install

// fitness-ai/backend
python -m venv myenv

// Windows
myenv\Scripts\activate
// Unix
source myenv/bin/activate

pip install -r requirements.txt
```

#### Postgres Initialization

Copy the `env.example` in `fitness-ai/backend` and rename it `.env`, change its configuration according to the file that will be sent separately (for security reasons)

> postgresql database is currently hosted for free in neon.tech

However, if you have postgresql installed in your local machine, you can edit the configuration in the `.env.example` according to your properties. And then paste it as an `.env`

    # from user to host, change it accordingly (.env.example)
    user="postgres"
    password="postgres"
    port="5432"
    host="localhost"
    dbname="workout_tracker" # dont change this
    is_local="True"  # dont change this. However, if you're going to use the hosted database, change it to "False"

## Usage guide

To start the application, run the startup script. It should automatically start up both the frontend and backend.

##### Windows

```
// fitness-ai/
start.bat
```

##### Unix (Linux/Mac)

```
// fitness-ai/
chmod +x start.sh
./start.sh
```

#### Manual Startup

```
// fitness-ai/frontend
npm run dev

// fitness-ai/backend

// Windows
myenv\Scripts\activate
// Unix
source myenv/bin/activate

python backend.py
```

![Login Page](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/Login.png)

Entering the frontend, you will be sent right away to the login and sign up page. First you'll have to sign up if you have no account. And log in if you do.

After logging in, you will be redirected to the dashboard. Everyday, a new exercise log is added to your account, where each iteration increases by 500 goal points, with an initial of 1000 goal points. The dashboard contains all the exercise logs you did every time you did a new day log in. It indicates if you've achieved you're goal for the specific day.

![Dashboard](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/Dashboard.png)

To add points for the day, you'll have to play the game while doing yoga exercises by click "Go to Game". After clicking the button, they will be redirected to the game window

![game_window](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/playgame.png)

To start the game, the user will have to upload an mp3 or wav file. The application will automatically detect the beats of the song and will synchronize the pose detection accordingly. The number of points added to your score will be depending on the confidence level detected by the model.

## Model Details

The Computer Vision model used is the pretrained YOLOv11n-pose model from Ultralytics. Alongside pose estimation, the model is also packaged with object detection, enabling the classification of objects. The model was fine-tuned using a publicly available [Yoga Poses Dataset](https://universe.roboflow.com/godviewai/workout_pose-46fqd/dataset/11) from Roboflow. There are a total of 2368 images in the dataset: 2190 train, 98 valid, and 80 test. The 4 classes included in the dataset are the Goddess, Plank, Tree, and Warrior-2 yoga poses, as shown below.

<p align="middle">
  <img src="https://github.com/AltairKazuto/fitness-ai/blob/master/frontend/public/goddess_pose.svg" width="200" />
  <img src="https://github.com/AltairKazuto/fitness-ai/blob/master/frontend/public/plank_pose.svg" width="200" /> 
  <img src="https://github.com/AltairKazuto/fitness-ai/blob/master/frontend/public/tree_pose.svg" width="200" />
  <img src="https://github.com/AltairKazuto/fitness-ai/blob/master/frontend/public/warrior2_pose.svg" width="200" />
</p>

The training involved standard parameters, with the number of epochs set to 200 and a patience of 20 to halt as the model converges. The training notebook can be found [here](https://github.com/AltairKazuto/fitness-ai/blob/yolo_training/yoga_pose_classifier_train.ipynb).

## Limitations and Future Improvements

1. Dataset Limitations

- Upon training the model, it was discovered that the keypoints in the dataset did not match the standard COCO skeleton format, resulting in mismatched joint connections and a high pose loss.
- There are only four classes, which introduces repetitiveness that is not ideal for a game-based application.

For future work, it is recommended to manually annotate a dataset such that formatting may be corrected and flexibility may be achieved in customizing the poses included in the game.

2. Model Selection

- In the current project, pose classification is actually done using YOLO's object detection and not using pose estimation. This is why, despite the improper joint mapping, the trained model was still able to classify the poses correctly. For improved realism and accuracy in pose matching, it is recommended to instead use MediaPipe in future work and create a benchmark model instead of using YOLO.

3. Beat Detection

- The current beat detection library used is too sensitive to sounds, other alternatives could be explored

2. Miscellaneous Improvements

- Selection of difficulty level.
- Introduction of multiplayer mode.

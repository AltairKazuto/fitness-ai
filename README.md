# Welcome to BEAT IT!

**Beat It** is an application in which users can do fun and engaging exercise activities at the comfort of their homes for free. This is a project for *CS 176 (2025-2026 1st Semester)*

**Members:**
Gabor, Ryv
Resano, Gabrielle
Rodriguez, Shaira

# Installation Guide

1. Clone the Repo to your local machine
2. Run `setup.bat` to install all the modules needed for the project (whether front-end or back-end)
3. Copy the `env.example` in the /backend/ and rename it `.env`, change its configuration according to the file that will be sent separately (for security reasons)
   > postgresql database is currently hosted for free in neon.tech

However, if you have postgresql installed in your local machine, you can edit the configuration in the `.env.example` according to your properties. And then paste it as an `.env`

    # from user to host, change it accordingly (.env.example)
    user="postgres"
    password="postgres"
    port="5433"
    host="localhost" 
    dbname="workout_tracker" # dont change this
    is_local="True"  # dont change this


## Usage guide

To run the application, go the root folder and run `windows_start.bat` if you're using Windows, `linux_start.bat` if you're using Linux/Mac. It should automatically start up the frontend and backend.

![Login Page](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/Login.png)

Entering the frontend, you will be sent right away to the login and sign up page. First you'll have to sign up if you have no account. And log in if you do. 

After logging in, you will be redirected to the dashboard. Everyday, a new exercise log is added to your account, where each iteration increases by 500 goal points, with an initial of 1000 goal points. The dashboard contains all the exercise logs you did every time you did a new day log in. It indicates if you've achieved you're goal for the specific day.

![Dashboard](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/Dashboard.png)

To add points for the day, you'll have to play the game while doing yoga exercises by click "Go to Game". After clicking the button, they will be redirected to the game window

![game_window](https://github.com/AltairKazuto/fitness-ai/blob/master/pictures/playgame.png)

To start the game, the user will have to upload an mp3 or wav file. The application will automatically detect the beats of the song and will synchronize the pose detection accordingly. The number of points added to your score will be depending on the confidence level detected by the model. 

## Model Details

## Limitations and Future Improvements

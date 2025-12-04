from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import DBConnector

app = FastAPI()
db = DBConnector()
db.connect()  


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/daily_logs")
def get_all_logs():
    return db.get_all_daily_logs()

@app.get("/daily_logs/{user_id}")
def get_logs_by_user(user_id: int):
    return db.get_daily_logs_by_user(user_id)
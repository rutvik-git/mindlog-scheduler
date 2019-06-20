from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import os
from flask import Flask
from pathlib import Path
from userdata_fetch_and_store import *
from mooddata_fetch_and_store import *
from notify_user import *

app = Flask(__name__)
@app.route("/")
def startup():
    user_data_update()
    mood_data_update()
    os.system("python run.py")
    return("Server Up and Running")

if __name__ == '__main__':
    app.run()

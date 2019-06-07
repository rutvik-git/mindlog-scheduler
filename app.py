from userdata_fetch_and_store import *
from mooddata_fetch_and_store import *
from notify_user import *
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import os
from flask import Flask

app = Flask(__name__)
@app.route("/")
def startup():
    os.system("python run.py")
    # return("Server Up and Running")

if __name__ == '__main__':
    app.run()

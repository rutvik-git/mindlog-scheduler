from run import *
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import os
from flask import Flask
from pathlib import Path

flag = False
app = Flask(__name__)
@app.route("/")
def startup():
    if(flag is True):
        print("Worker Process Running...")
        user_data_update()
        mood_data_update()
        startup()
        schedule_new_users()
        print("Startup Processes Complete...")
        p1 = Process(target=user_data_scheduler)
        p1.start()
        p2 = Process(target=mood_data_scheduler)
        p2.start()
        p3 = Process(target=all_users_notification_scheduler)
        p3.start()
        p4 = Process(target=check_eligibility_scheduler)
        p4.start()
        print("Primary Processes Schedule Complete...")
    flag = True
    return("Server Up and Running")
    # exec(Path("run.py").read_text())

if __name__ == '__main__':
    # os.system("python run.py")
    app.run()

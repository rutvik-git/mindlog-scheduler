from userdata_fetch_and_store import *
from mooddata_fetch_and_store import *
from notify_user import *
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import os
from flask import Flask
import logging
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

def user_data_scheduler():
    sched = BlockingScheduler()
    sched.add_job(user_data_update, 'interval', seconds=15)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)

def mood_data_scheduler():
    sched = BlockingScheduler()
    sched.add_job(mood_data_update, 'interval', seconds=15)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)

def all_users_notification_scheduler():
    sched = BlockingScheduler()
    sched.add_job(schedule_new_users, 'interval', minutes=1)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)

app = Flask(__name__)
@app.route("/")
def startup():
    os.system("python app_test.py")

    return("Server Up and Running")

if __name__ == '__main__':
    app.run()

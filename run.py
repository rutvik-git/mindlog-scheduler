from userdata_fetch_and_store import *
from mooddata_fetch_and_store import *
from notify_user import *
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Process, Queue
import os
from flask import Flask
# import logging
# log = logging.getLogger('apscheduler.executors.default')
# log.setLevel(logging.INFO)
# fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
# h = logging.StreamHandler()
# h.setFormatter(fmt)
# log.addHandler(h)

def user_data_scheduler():
    sched = BlockingScheduler()
    sched.add_job(user_data_update, 'interval', minutes=1)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)

def mood_data_scheduler():
    sched = BlockingScheduler()
    sched.add_job(mood_data_update, 'interval', minutes=1)
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

def check_eligibility():
        LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
        local = pg.connect(LOCAL_DATABASE, sslmode='require')
        local_cur = local.cursor()
        local_cur.execute('select username from userdata');
        users = np.squeeze(local_cur.fetchall())
        for user in users:
            local_cur.execute("select * from userdata where username='%s'"%(user))
            result = local_cur.fetchone()
            join_date = result[5]
            curr_date = dt.datetime.now().date()
            diff = (curr_date - join_date).days
            if(diff>14):
                local_cur.execute("update userdata set valid_user = FALSE where username='%s'"%(user))
            local.commit()

def check_eligibility_scheduler():
    sched = BlockingScheduler()
    sched.add_job(check_eligibility, 'interval', minutes=1)
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown(wait=False)

def startup():
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute('select username from userdata');
    users = np.squeeze(local_cur.fetchall())
    for user in users:
        local_cur.execute("select * from userdata where username='%s'"%(user))
        result = local_cur.fetchone()
        join_date = result[5]
        curr_date = dt.datetime.now().date()
        diff = (curr_date - join_date).days
        if(diff<14):
            local_cur.execute("update userdata set scheduled = FALSE where username='%s'"%(user))
        else:
            local_cur.execute("update userdata set valid_user = FALSE where username='%s'"%(user))
        local.commit()

print("Worker Process Running...")
user_data_update()
mood_data_update()
startup()
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

import os
import datetime as dt
import numpy as np
import psycopg2 as pg
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib, ssl
import threading

import logging
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

global carriers
carriers = {
    'att': '@mms.att.net',
    'tmobile': '@tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nexel.com',
    'googlefi':'@msg.fi.google.com',
    'virginmobile':'@vmobl.com',
    'uscellular':'@email.uscc.net',
    'cricket':'@sms.mycricket.com',
    'boostmobile':'@sms.myboostmobile.com'
}

global curr_dir
curr_dir = os.path.dirname(os.path.realpath('__file__'))

def info(user, type, time):
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute("insert into server_logs values(DEFAULT, '%s', '%s', '%s')" % (user, type, time))
    local.commit()

def send_message(user, contact, carrier, message):
    port = 465
    password = "neatlabs-mindlog"
    smtp_server = "smtp.gmail.com"
    sender_email = "mindlog.neatlabs@gmail.com"
    context =  ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    to_number = (str(contact)+'{}').format(carriers[str(carrier)])
    try:
        server.sendmail(sender_email, to_number, message)
        info(user,'user notification',dt.datetime.now())
    except:
        pass
    server.quit()

def msg(user):
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute('select username from userdata');
    users = np.squeeze(local_cur.fetchall())
    if user in users:
        local_cur.execute("select contact from userdata where username='%s'"%(user))
        contact = np.squeeze(local_cur.fetchone())
        local_cur.execute("select carrier from userdata where username='%s'"%(user))
        carrier = np.squeeze(local_cur.fetchall())
        message = 'Please fill your mindlog\n' + 'https://pythonserver-neatlabs.herokuapp.com/mindlog/' + str(user) + ' (notification for timestamp : ' + str(dt.datetime.now()) + ')'
        send_message(user, str(contact), carrier, message)

def schedule_user(user):
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute("select scheduled from userdata where username ='%s'"%(user))
    isScheduled = bool(np.squeeze(local_cur.fetchone()))

    if(isScheduled is False):
        local_cur.execute("select wakeup_time, sleep_time, join_date from userdata where username='%s'"%(user))
        wakeup_time, sleep_time, join_date = local_cur.fetchone()
        start = (wakeup_time.hour)*60 + wakeup_time.minute
        end = (sleep_time.hour)*60 + sleep_time.minute
        notif_times = np.linspace(start, end, 4, dtype=np.int16)
        scheduler = BlockingScheduler()
        d = dt.timedelta(days = 14)
        last_date = join_date + d
        user_schedules = []
        for time in notif_times:
            h = int(time/60)
            m = int(time%60)
            user_schedules.append("%s:%s"%(h,m))
            scheduler.add_job(msg, 'cron', hour=h, minute=m, start_date=join_date, end_date=last_date, args=[user])
        info(user, 'user scheduled at ' + str(user_schedules), dt.datetime.now())
        print(user,'scheduled at', user_schedules)
        local_cur.execute("UPDATE userdata SET scheduled = TRUE WHERE username = '%s'"%(user))
        local.commit()
        scheduler.start()

def schedule_new_users():
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute("select username, scheduled from userdata")
    user_list = local_cur.fetchall()
    for item in user_list:
        user = item[0]
        isScheduled = bool(item[1])
        if(isScheduled is False):
            t = threading.Thread(target=schedule_user, args=(user,))
            t.start()

import os
import datetime as dt
import numpy as np
import pandas as pd
import smtplib, ssl

global carriers
carriers = {
    'att': '@mms.att.net',
    'tmobile': '@tmomail.net',
    'verizon': '@vtext.com',
    'sprint': '@page.nexel.com',
    'googlefi':'',
    'virginmobile':'',
    'uscellular':'',
    'cricket':'',
    'boostmobile':''
}

global curr_dir
curr_dir = os.path.dirname(os.path.realpath('__file__'))

def info(title):
    f = open(os.path.join(curr_dir, 'mindlog-server-logs.txt'), "a")
    f.write(title + '\t' + 'parent process: ' + str(os.getppid()) + '\t' + 'process id: ' + str(os.getpid()) + '\n')
    f.close()

def send_message(contact, carrier, message):
    port = 465
    password = "neatlabs-mindlog"
    smtp_server = "smtp.gmail.com"
    sender_email = "mindlog.neatlabs@gmail.com"
    context =  ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.login(sender_email, password)
    to_number = (str(contact)+'{}').format(carriers[str(carrier)])
    # server.sendmail(sender_email, to_number, message)
    server.quit()
    print(sender_email, to_number, message)

def msg(user):
    df = pd.read_csv('user_data.csv')

    if user in df['username'].values:
        contact = (df[df['username']==user].iloc[0]['contact'])
        carrier = (df[df['username']==user].iloc[0]['carrier'])
        message = 'Please fill your mindlog\n' + 'https://pythonserver-neatlabs.herokuapp.com/mindlog' + ' (notification for timestamp : ' + str(dt.datetime.now()) + ')'
        send_message(str(contact), carrier, message)
        f = open(os.path.join(curr_dir, str(user)+"_logs.txt"), "a")
        f.write(user+'-notified@'+str(dt.datetime.now()) + '\n')
        f.close()
        info(user+'-notified@'+str(dt.datetime.now()))
        
msg('killer')

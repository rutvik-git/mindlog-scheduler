import os
import datetime as dt
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib, ssl
import threading

port = 465
password = "TeamBrainE20!("
smtp_server = "smtp.ucsd.edu"
sender_email = "neatlabs@ucsd.edu"
context =  ssl.create_default_context()
server = smtplib.SMTP_SSL(smtp_server, port)
server.ehlo()
server.login(sender_email, password)
server.sendmail(sender_email, '8582322855@msg.fi.google.com', 'test message')
server.quit()

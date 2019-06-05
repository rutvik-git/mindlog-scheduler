import os
import psycopg2 as pg
import psycopg2.extras as pge
import datetime as dt
import numpy as np
import pandas as pd

global select_all_query, curr_dir
curr_dir = os.path.dirname(os.path.realpath('__file__'))
select_all_query = 'SELECT * from %s'

def info(title):
    f = open(os.path.join(curr_dir, 'mindlog-server-logs.txt'), "a")
    f.write(title + '\t' + 'parent process: ' + str(os.getppid()) + '\t' + 'process id: ' + str(os.getpid()) + '\n')
    f.close()

def mood_data_update():
    os.environ["DATABASE_URL"] = "postgres://ysnnfooijfyqpq:2255172969ba42378ca61ed80e5a001c4166d40005544e66ceea5350efeb401c@ec2-174-129-240-67.compute-1.amazonaws.com:5432/d75eoc3l0g0qpu"
    DATABASE_URL = os.environ['DATABASE_URL']
    try:
        conn = pg.connect(DATABASE_URL, sslmode='require')
    except:
        print("Connection Error. Try Again.")

    cur = conn.cursor()
    table_name = 'mooddata'
    cur.execute(select_all_query % table_name)
    rows = cur.fetchall()
    df = pd.DataFrame(columns=['breath_data', 'time', 'username', 'responses'])

    i = 1
    for row in rows:
        df.loc[i] = (row[1], row[2], row[3], row[4])
        i += 1
    df.to_csv('mood_data.csv')
    info("mood-data-fetch&store@"+str(dt.datetime.now()))

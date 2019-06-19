import os
import psycopg2 as pg
import psycopg2.extras as pge
import datetime as dt
import numpy as np

global select_all_query, curr_dir, insert_query
curr_dir = os.path.dirname(os.path.realpath('__file__'))
select_all_query = 'SELECT * from %s'
insert_query = 'INSERT INTO %s VALUES(%s)'

def info(user, type, time):
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute("insert into server_logs values(DEFAULT, '%s', '%s', '%s')" % (user, type, time))
    local.commit()

def mood_data_update():
    os.environ["EXTERNAL_DATABASE"] = "postgres://ysnnfooijfyqpq:2255172969ba42378ca61ed80e5a001c4166d40005544e66ceea5350efeb401c@ec2-174-129-240-67.compute-1.amazonaws.com:5432/d75eoc3l0g0qpu"
    EXTERNAL_DATABASE = os.environ['EXTERNAL_DATABASE']
    conn = pg.connect(EXTERNAL_DATABASE, sslmode='require')
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')

    cur = conn.cursor()
    table_name = 'mooddata'
    cur.execute(select_all_query % table_name)
    rows = cur.fetchall()

    local_cur = local.cursor()

    for row in rows:
        values = "'%s','%s', '%s', '%s', '%s'" % (row[0],row[1],row[2],row[3],row[4])
        try:
            local_cur.execute(insert_query % ('mindlog', values))
            local.commit()
        except:
            pass
    info("not user specific","mindlog data fetch and store",dt.datetime.now())

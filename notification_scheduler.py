from mindlog_functions import *
def startup():
    print('Startup Start...')
    # user_data_update()
    # mood_data_update()
    LOCAL_DATABASE = "postgres://vlbetxrecjmcay:801d255c4b4ae13e105d06c4220a972254e65d935edbfba6f31493f133b91764@ec2-50-19-114-27.compute-1.amazonaws.com:5432/dfqi93sufn0631"
    local = pg.connect(LOCAL_DATABASE, sslmode='require')
    local_cur = local.cursor()
    local_cur.execute('select username from userdata');
    users = np.squeeze(local_cur.fetchall())
    if (type(users) is not list):
        temp = users
        users = [temp]
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
    print('Startup Process Complete...')
startup()
print('User Notification Scheduled...')
all_users_notification_scheduler()

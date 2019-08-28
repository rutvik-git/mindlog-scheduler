from mindlog_functions import *


schedule_new_users()
# sched = BlockingScheduler()
# sched.add_job(schedule_new_users, 'interval', minutes=5)
# try:
#     sched.start()
# except (KeyboardInterrupt, SystemExit):
#     sched.shutdown(wait=False)

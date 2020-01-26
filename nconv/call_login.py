"""
@File : call_login.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/24
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from nconv.sc import new_load
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(new_load,  'interval', hours=1, start_date='2020-01-26 14:35:00', end_date='2020-06-15 11:00:00')
scheduler.start()
print('程序开始执行！')
print('发送邮件！')

"""
@File : call_login.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/24
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from nconv.scary_conv import load_conv
# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(load_conv, 'interval', seconds=1800)
scheduler.start()
print('程序开始执行！')
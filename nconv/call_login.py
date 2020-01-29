"""
@File : call_login.py
@copyright : GG
@Coder: Leslie_s
@Date: 2020/1/24
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from datetime import datetime
from nconv.sc import new_load
from nconv.pyecharts import map_img,summary_qg
import logging

'''
  scheduler.remove_job(job_id,jobstore=None)#删除作业
  2   scheduler.remove_all_jobs(jobstore=None)#删除所有作业
  3   scheduler.pause_job(job_id,jobstore=None)#暂停作业
  4   scheduler.resume_job(job_id,jobstore=None)#恢复作业
'''
# 输出时间
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S',
                        filename='log1.txt',
                        filemode='a')
def my_listener(event):
        if event.exception:
            print ('任务出错了！！！！！！')
        else:
            print ('任务照常运行...')
scheduler = BlockingScheduler()
scheduler.add_job(map_img, 'interval', hours=1, start_date='2020-01-29 13:58:00', end_date='2020-06-15 11:00:00')
scheduler.add_job(new_load, 'interval', hours=1, start_date='2020-01-29 13:59:00', end_date='2020-06-15 11:00:00')
scheduler.add_job(summary_qg,'interval', hours=24, start_date='2020-01-29 23:59:59', end_date='2020-06-15 11:00:00')
scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler._logger = logging
scheduler.start()
print('程序开始执行！')
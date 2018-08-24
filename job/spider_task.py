import time
import schedule
from util import job_util
from spider import kuaidaili
from spider import xici


def job():
    job_util.set_job_kv('spider_task', True)
    kuaidaili.run()
    xici.run()
    job_util.set_job_kv('spider_task', False)


def spider_job_run(job_time='00:00'):
    schedule.every().day.at(job_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

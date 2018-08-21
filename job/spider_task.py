import schedule
import time
from spider import kuaidaili


def job():
    kuaidaili.run()


def spider_job_run(job_time='00:00'):
    schedule.every().day.at(job_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

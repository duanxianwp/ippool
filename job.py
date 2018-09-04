import time
import schedule
import threading
from job import ip_keep_alive_task
from job import spider_task

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every().day.at('00:00').do(run_threaded, spider_task.job)
schedule.every(2).hours.do(run_threaded, ip_keep_alive_task.job)

while 1:
    schedule.run_pending()
    time.sleep(1)
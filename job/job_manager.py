from job import spider_task
from job import ip_keep_alive_task

'''job总开关'''


def run():
    spider_task.spider_job_run("00:00")
    ip_keep_alive_task.keep_alive_job()

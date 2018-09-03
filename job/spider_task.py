from util import job_util
from spider import kuaidaili
from spider import xici


def job():
    job_util.set_job_kv('spider_task', True)
    kuaidaili.run()
    xici.run()
    job_util.set_job_kv('spider_task', False)

import schedule
import time
from util import ip_util
from util import job_util
from job import spider_task
from db import mongo_driver

# 爬虫job执行的时间与当前时间的差值大于这个值就 执行
time_out = 60 * 60


def job():
    mongo = mongo_driver.MongoDB()
    client = mongo.get_client()
    tb = mongo.get_table_by_db_and_tb('ippool', 'iprecord', client)
    for item in tb.find():
        if not ip_util.is_success(item):
            tb.delete_one({'ip': item['ip'], 'port': item['port']})
    count = tb.find().count()
    client.close()
    if count < 500:
        spider_job = job_util.get_job_kv('spider_task')
        if (spider_job is None) or (
                (spider_job['status'] is False) and (spider_job['update_at'] - time.time() > time_out)):
            spider_task.job()


def keep_alive_job():
    schedule.every(2).hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


job()

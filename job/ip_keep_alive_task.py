import schedule
import time
from db import mongo_driver
from job import spider_task
from util import ip_validate


def job():
    mongo = mongo_driver.MongoDB()
    tb = mongo.get_table_by_db_and_tb('ippool', 'iprecord')
    for item in tb.find():
        if not ip_validate.is_success(item):
            tb.delete_one({'ip': item['ip'], 'port': item['port']})
    if tb.find().count() < 500:
        spider_task.job()


def keep_alive_job():
    schedule.every(2).hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

import schedule
import time
from util import ip_util
from util import job_util
from db import mongo_driver


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
        job_util.notify_spider_run()


def keep_alive_job():
    schedule.every(2).hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

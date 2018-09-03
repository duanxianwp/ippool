from db.mongo_driver import MongoDB
from util import ip_util
from util import job_util
import random


def get_ip():
    mongo = MongoDB()
    client = mongo.get_client()
    tb = mongo.get_table_by_db_and_tb('ippool', 'ip_record', client)
    while True:
        count = tb.find().count()
        it = tb.find().limit(1).skip(random.randint(0, count))
        record = it.next()
        if record is None:
            job_util.notify_spider_run()
            raise Exception("ip资源不足")
        if ip_util.is_success(record):
            return record

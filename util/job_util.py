from db.mongo_driver import MongoDB
import time

mongo = MongoDB()


def set_job_kv(job_name, status):
    client = mongo.get_client()
    tb = mongo.get_table_by_db_and_tb('ippool', 'job', client)
    item = {
        'name': job_name,
        'status': status,
        'update_at': time.time()
    }
    tb.find_and_modify(item, upsert=True)
    client.close()


def get_job_kv(job_name):
    client = mongo.get_client()
    tb = mongo.get_table_by_db_and_tb('ippool', 'job', client)
    item = {
        'name': job_name
    }
    item = tb.find_one(item)
    client.close()
    return item


def notify_spider_run():
    spider_job = job_util.get_job_kv('spider_task')
    if (spider_job is None) or (
            (spider_job['status'] is False) and (spider_job['update_at'] - time.time() > time_out)):
        spider_task.job()

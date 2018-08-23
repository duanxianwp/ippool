from db.mongo_driver import MongoDB
import time

mongo = MongoDB()


def set_job_kv(job_name, status):
    tb = mongo.get_table_by_db_and_tb('ippool', 'job')
    item = {
        'name': job_name,
        'status': status,
        'update_at': time.time()
    }
    tb.find_and_modify(item, upsert=True)


def get_job_kv(job_name):
    tb = mongo.get_table_by_db_and_tb('ippool', 'job')
    item = {
        'name': job_name
    }
    return tb.find_one(item)

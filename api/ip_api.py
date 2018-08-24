from db.mongo_driver import MongoDB


def get_ip():
    mongo = MongoDB()
    client = mongo.get_client()
    tb = mongo.get_table_by_db_and_tb('ippool', 'ip_record', client)
    record = tb.find_one()
    return record

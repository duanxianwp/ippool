import requests
from db.mongo_driver import MongoDB

mongo = MongoDB()

'''ip可用性检查'''


def is_success(item):
    try:
        _url = 'https://www.baidu.com'
        session = requests.session()
        session.proxies = {'http': '{}:{}'.format(item['ip'], item['port'])}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'}
        session.get(_url, timeout=10, headers=headers)
    except BaseException as e:
        return False
    return True


def store_ip(item):
    '''检查是否可用'''
    if not is_success(item):
        return
    try:
        client = mongo.get_client()
        db = mongo.get_database(client, 'ippool')
        tb = mongo.get_table(db, 'ip_record')
        '''检查是否已存在'''
        if tb.find_one({'ip': item['ip']}) is None:
            tb.insert_one(item)
    except Exception as e:
        # 日志就不打印了
        pass
    finally:
        client.close()

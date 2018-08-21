import requests
from bson import ObjectId
from bs4 import BeautifulSoup
from multiprocessing import Pool
from db.mongo_driver import MongoDB

mongo = MongoDB()


def get_ip(page):
    url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    ips = soup.select('.table > tbody > tr > td:nth-of-type(1)')
    ports = soup.select('.table > tbody > tr > td:nth-of-type(2)')
    item = {}
    for ip, port in zip(ips, ports):
        item['ip'] = ip.text
        item['port'] = port.text
        '''生成唯一ID'''
        item['_id'] = ObjectId().from_datetime()
        print(item)
        store_ip(item)


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


def run():
    begin = 1
    end = 100
    pool = Pool()
    pool.map(get_ip, [page for page in range(begin, end + 1)])
    pool.close()

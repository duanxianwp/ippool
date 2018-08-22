import copy
import requests
from db import ip_validate
from bs4 import BeautifulSoup
from multiprocessing import Pool
from db.mongo_driver import MongoDB

mongo = MongoDB()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def get_ip(page):
    url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
    source = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source, 'lxml')
    ips = soup.select('.table > tbody > tr > td:nth-of-type(1)')
    ports = soup.select('.table > tbody > tr > td:nth-of-type(2)')
    item = {}
    for ip, port in zip(ips, ports):
        item['ip'] = ip.text
        item['port'] = port.text
        '''使用copy'''
        store_ip(copy.copy(item))


def store_ip(item):
    '''检查是否可用'''
    if not ip_validate.is_success(item):
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


def run():
    begin = 1
    end = 100
    pool = Pool()
    pool.map(get_ip, [page for page in range(begin, end + 1)])
    pool.close()


run()

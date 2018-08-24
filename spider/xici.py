import copy
import requests
from util import ip_util
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import Lock

lock = Lock()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def query_and_store_ip(page):
    items = []
    items.extend(get_nn_ip(page))
    items.extend(get_nt_ip(page))
    items.extend(get_wn_ip(page))
    items.extend(get_wt_ip(page))
    for item in items:
        lock.acquire()
        ip_util.store_ip(item)
        lock.release()


def get_nn_ip(page):
    url = 'http://www.xicidaili.com/nn/{}'.format(page)
    return get_ip(url, page)


def get_nt_ip(page):
    url = 'http://www.xicidaili.com/nt/{}'.format(page)
    return get_ip(url, page)


def get_wn_ip(page):
    url = 'http://www.xicidaili.com/wn/{}'.format(page)
    return get_ip(url, page)


def get_wt_ip(page):
    url = 'http://www.xicidaili.com/wt/{}'.format(page)
    return get_ip(url, page)


def get_ip(url, page):
    source = requests.get(url, headers=headers).text

    if source == '-10':
        return get_ip(url, page)
    soup = BeautifulSoup(source, 'lxml')
    ips = soup.select('#ip_list > tr > td')[1::10]
    ports = soup.select('#ip_list > tr > td')[2::10]
    items = []
    item = {}
    for ip, port in zip(ips, ports):
        item['ip'] = ip.text
        item['port'] = port.text
        items.append(copy.copy(item))
    return items


def run():
    begin = 1
    end = 100
    pool = Pool()
    pool.map(query_and_store_ip, [page for page in range(begin, end + 1)])
    pool.close()

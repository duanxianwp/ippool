import requests

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

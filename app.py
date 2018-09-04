from asyncio import log

from flask import Flask, request, url_for
from api.ip_api import get_ip

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/get')
def ip_api():
    try:
        ip = str(get_ip())
        return ip
    except Exception as e:
        return str(e)


@app.route('/del', methods=['GET'])
def del_ip():
    ip = request.args.get('ip')
    port = request.args.get('port')
    item = {
        'ip': ip,
        'port': port
    }
    try:
        del_ip(item)
    except Exception as e:
        pass
    return 'SUCCESS'


if __name__ == '__main__':
    app.run(port=8081)

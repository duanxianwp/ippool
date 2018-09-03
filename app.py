from flask import Flask
from api.ip_api import get_ip

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api')
def ip_api():
    try:
        ip = str(get_ip())
        return ip
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(port=8081)

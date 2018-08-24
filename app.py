from flask import Flask
from api.ip_api import get_ip

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api')
def ip_api():
    return str(get_ip())


if __name__ == '__main__':
    app.run()

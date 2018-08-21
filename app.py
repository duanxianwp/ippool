from flask import Flask
from job import job_manager

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/job')
async def run_job():
    await job_manager.run()
    return "haha"


if __name__ == '__main__':
    app.run()

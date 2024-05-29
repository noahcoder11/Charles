from flask import Flask, request
import os
import json
from .system_functions import * 
import logging

app = Flask(__name__, static_url_path='', static_folder='web_ui')

def update_code():
    os.system('git pull origin master')


@app.route('/update-code', methods=['POST'])
def update_code():
    update_charles_code()
    return json.dumps({})

@app.route('/config', methods=['GET', 'POST'])
def configure():
    if request.method == 'GET':
        return json.dumps( get_charles_config() )
    data = request.get_json()
    print(data)
    input_device_index = data.get('input_device_index', 0)
    output_device_index = data.get('output_device_index', 0)
    server_url = data.get('server_url', 'http://127.0.0.1:5000')
    configure_charles(input_device_index=input_device_index, output_device_index=output_device_index, server_url=server_url)
    return json.dumps({})

@app.route('/logs', methods=['GET'])
def api_get_logs():
    return json.dumps({ 'logs': get_logs() })

@app.route('/test-audio', methods=['POST'])
def test_audio():
    data = request.get_json()
    device_index = data.get('device_index', 0)
    test_output_audio(device_index)
    return json.dumps({})

@app.route('/')
def index():
    print(os.getcwd())
    return app.send_static_file('index.html')


def run_server():
    app.run(port=5000, host='0.0.0.0')
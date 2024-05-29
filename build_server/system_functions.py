from subprocess import Popen
import os
import time
import dotenv
from modules import logging
import threading
import sounddevice
from playsounds import playsound

logger = logging.Logger(code='SERVER')
dotenv_file = dotenv.find_dotenv()

def track_os_command_process(process):
    while process.poll() is None:
        time.sleep(1)
        logger.log('.', newline=False)

    logger.log('done')

def start_asynchronous_command(command):
    process = Popen(command.split(' '))
    thread = threading.Thread(target=track_os_command_process, args=(process,))
    thread.start()

def update_charles_code():
    logger.log('Updating Charles code:')
    os.system('git pull origin master')
    logger.log('- Repo cloned')
    os.system('chmod +x ./install.sh')
    logger.log('- Install script made executable')
    logger.log('- Running install script', newline=False)
    start_asynchronous_command('./install.sh')

def restart_charles():
    logger.log('Restarting Charles:')
    os.system('systemctl restart charles')
    logger.log('- Charles restarted')

def configure_charles(input_device_index=0, output_device_index=0, server_url='http://127.0.0.1:5000'):
    logger.log('Configuring Charles:')
    dotenv.set_key(dotenv_file, 'CHARLES_INPUT_AUDIO_DEVICE', str(input_device_index))
    dotenv.set_key(dotenv_file, 'CHARLES_OUTPUT_AUDIO_DEVICE', str(output_device_index))
    dotenv.set_key(dotenv_file, 'CHARLES_MONITOR_URL', server_url)
    logger.log('- Charles configured')
    dotenv.load_dotenv()
    restart_charles()

def get_charles_config():
    dotenv.load_dotenv()
    env_vars = dotenv.dotenv_values()
    input_device_index = env_vars.get('CHARLES_INPUT_AUDIO_DEVICE', None)
    output_device_index = env_vars.get('CHARLES_OUTPUT_AUDIO_DEVICE', None)
    server_url = env_vars.get('CHARLES_MONITOR_URL', 'http://127.0.0.1:5000')

    available_devices = sounddevice.query_devices()

    return {
        'input_device_index': input_device_index,
        'output_device_index': output_device_index,
        'server_url': server_url,
        'available_devices': available_devices
    }

def test_output_audio(device_index):
    playsound('sounds/Charles_Startup.wav', output_device_index=device_index)

def get_logs():
    return logger.fetch_logs()

def clear_logs():
    logger.clear()
    
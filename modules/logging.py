import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class Logger:
    def __init__(self, code=None):
        self.path = os.environ.get('CHARLES_LOG_PATH', 'charles_log.txt')
        self.code = code

    def clear(self):
        with open(self.path, 'w') as f:
            f.write('')

    def log(self, message, newline=True):
        with open(self.path, 'a') as f:
            if self.code:
                f.write('{0} | {1}: {2}{3}'.format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), self.code, message, '\\n' if newline else ''))
            else:
                f.write('{0} | INFO: {1}{2}'.format(datetime.now().strftime('%d-%m-%Y %H:%M:%S'), message, '\\n' if newline else ''))

    def fetch_logs(self):
        data = ''
        with open(self.path, 'r') as f:
            data = f.read()
        return data
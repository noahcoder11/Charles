import requests

class Generator:
    def __init__(self, url):
        self.url = url

    def generate(self):
        return requests.get(self.url).text
# https://console.leancloud.cn/apps/8alQIE7rUNqk6Y7DqxPgrJvK-gzGzoHsz/storage/data/options
import requests
import os

BASE_URL = 'https://8alqie7r.lc-cn-n1-shared.com/1.1/classes/options'


class LcOption:
    def __init__(self, **kwargs):
        self.headers = {'X-LC-Id': kwargs.get('app_id', os.getenv('LC_ID')),
                        'X-LC-Key': kwargs.get('app_key', os.getenv('LC_KEY')),
                        'Content-Type': 'application/json'}

    def get(self, id, **kwargs):
        url = f'{BASE_URL}/{id}'
        res = requests.get(url, headers=self.headers, **kwargs)
        return self.process_response(res)

    def post(self, id, **kwargs):
        url = f'{BASE_URL}/{id}'
        data = kwargs.get('data', {})
        res = requests.post(url, headers=self.headers, json=data, **kwargs)
        return self.process_response(res)

    @classmethod
    def process_response(cls, res):
        if res.status_code == 200:
            return res.json()
        return None

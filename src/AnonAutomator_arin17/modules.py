import os
import json
import random
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


class SecretM:
    def __init__(self, uid=None, messages=None):
        self._base_url = 'https://secretm.me'
        self._page = 'message_h.php'
        self.uid = uid
        self.messages = messages
        self.load_messages()

    def load_messages(self) -> None:
        if self.messages is None:
            with open(os.path.join(Path(__file__).resolve().parent, 'resources', 'messages.json'), 'r') as fp:
                self.messages = json.load(fp)
        return

    def get_full_url(self) -> str:
        return '/'.join((self._base_url, self._page))

    def get_message(self) -> str:
        key = random.choice(tuple(self.messages.keys()))
        return random.choice(self.messages[key])

    def prepare_payload(self) -> dict:
        res = {
            'name': str(self.uid),
            'ans1': self.get_message(),
            'agree': 'on'
        }
        return res

    def _post(self, idx: int) -> None:
        payload = self.prepare_payload()
        res = requests.post(url=self.get_full_url(), data=payload)
        print("Response- {:03d}({}): {}".format(idx, res.status_code, payload['ans1'].strip()))

    def post(self, n: int = 1):
        with ThreadPoolExecutor() as executor:
            executor.map(self._post, range(1, n + 1))

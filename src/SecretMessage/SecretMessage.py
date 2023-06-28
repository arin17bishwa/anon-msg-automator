from abc import ABC
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from base.BaseMessageAutomator import BaseMessageAutomator


class SecretMessageAutomator(BaseMessageAutomator, ABC):
    def __init__(self, uid: str, *args, **kwargs):
        actual_uid = self.get_actual_post_id(temp_uid=uid)
        super().__init__(actual_uid, *args, **kwargs)

    @staticmethod
    def get_actual_post_id(temp_uid: str) -> str:
        url = f"https://www.secretmessage.link/secret/{temp_uid}"
        home_soup = BeautifulSoup(requests.get(url).text, features="html.parser")
        body_attrs = home_soup.body.attrs
        for class_attr in body_attrs.get('class', []):
            if class_attr.startswith('postid-'):
                return class_attr.split('-')[-1]
        return ''

    @staticmethod
    def parsable_patterns() -> List[str]:
        patterns = [
            r"^https:\/\/www\.secretmessage\.link\/secret\/(?P<uid>[a-z0-9]+)\/?$",
            r"^(?P<uid>[a-z0-9]+)$",
        ]
        return patterns

    @property
    def _posting_url(self):
        return "https://www.secretmessage.link/wp-admin/admin-ajax.php"

    def prepare_payload(self, message: str) -> Dict:
        payload = {
            'action': "update_secret_msg",
            'message': message,
            'postId': self.uid
        }
        return payload

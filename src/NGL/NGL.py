import uuid
from abc import ABC
from typing import List, Dict

from base.BaseMessageAutomator import BaseMessageAutomator


class NGLAutomator(BaseMessageAutomator, ABC):
    @staticmethod
    def parsable_patterns() -> List[str]:
        patterns = [
            r"/^https:\/\/confess\.ngl\.link\/(?P<uid>[a-z0-9_\.]+)\/?$",
            r"(?P<uid>[a-z0-9_]+)",
        ]
        return patterns

    @property
    def _posting_url(self):
        return 'https://ngl.link/api/submit'

    @staticmethod
    def _generate_random_device_id() -> str:
        return str(uuid.uuid4())

    def prepare_payload(self, message: str) -> Dict:
        payload = {
            'username': self.uid,
            'question': message,
            'deviceId': self._generate_random_device_id(),
            'gameSlug': 'confessions',
        }

        return payload

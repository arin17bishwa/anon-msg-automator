from abc import ABC
from typing import Dict

from base.BaseMessageAutomator import BaseMessageAutomator


class StoryZInkAutomator(BaseMessageAutomator, ABC):
    @property
    def _posting_url(self) -> str:
        return "https://storyzink.com/message_h.php"

    def prepare_payload(self, message: str) -> Dict:
        return {
            'name': str(self.uid),
            'ans1': message,
            'agree': 'on'
        }

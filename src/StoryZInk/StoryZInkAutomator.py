from abc import ABC
from typing import Dict, List

from base.BaseMessageAutomator import BaseMessageAutomator


class StoryZInkAutomator(BaseMessageAutomator, ABC):
    @staticmethod
    def parsable_patterns() -> List[str]:
        patterns = [
            r"^https:\/\/storyzink\.com\/m\/(?P<uid>[a-z0-9]{8,8})\/?$",
            r"^(?P<uid>[a-z0-9]{8,8})",
        ]
        return patterns

    @property
    def _posting_url(self) -> str:
        return "https://storyzink.com/message_h.php"

    def prepare_payload(self, message: str) -> Dict:
        return {
            'name': str(self.uid),
            'ans1': message,
            'agree': 'on'
        }

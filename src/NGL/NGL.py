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


def main():
    txt = 'mr_prokaryot1'
    txt = '_.b.soumik._'
    # txt = 'https://confess.ngl.link/mr_prokaryot1'
    message_types = ['smooth']
    verbose_level = 2
    spammer = NGLAutomator.get_obj_from_text(txt, message_types=message_types, verbose_level=verbose_level)
    n = 3
    spammer.spam(n)
    print(spammer.uid, spammer.message_types, spammer.verbose_level)


if __name__ == "__main__":
    main()

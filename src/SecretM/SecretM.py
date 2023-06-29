from typing import List

from StoryZInk.StoryZInkAutomator import StoryZInkAutomator


class SecretMAutomator(StoryZInkAutomator):
    @staticmethod
    def parsable_patterns() -> List[str]:
        patterns = [
            r"^https:\/\/storyzink\.com\/m\/(?P<uid>[a-z0-9]{8,8})\?s=2$",  # the last ?s=2 part is the only difference
            r"^(?P<uid>[a-z0-9]{8,8})",
        ]
        return patterns

    @property
    def _posting_url(self) -> str:
        return "https://secretm.me/message_h.php"

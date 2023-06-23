from typing import Optional
from base.BaseMessageAutomator import BaseMessageAutomator
from StoryZInk import StoryZInkAutomator

SPAMMERS = [
    StoryZInkAutomator.StoryZInkAutomator,
]


def get_spammer(text: str, *args, **kwargs) -> Optional[BaseMessageAutomator]:
    for cls in SPAMMERS:
        spammer = cls.get_obj_from_text(text, *args, **kwargs)
        if spammer:
            return spammer
    return

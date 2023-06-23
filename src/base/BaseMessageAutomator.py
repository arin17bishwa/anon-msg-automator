import itertools
import json
import logging
import os
import random
import re
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
# from itertools import chain, cycle
from typing import List, Dict, Optional, Iterable

import requests

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(level=20)

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseMessageAutomator(ABC):
    def __init__(self, uid: str, message_types: Optional[Iterable[str]] = None, verbose_level: int = 1, *args,
                 **kwargs):
        if message_types is None:
            message_types = tuple()
        self._uid: str = uid
        # self.fp: Optional[TextIO] = None
        self.messages: Dict[str, List[str]] = {}
        self.message_types: Iterable[str] = message_types
        self.load_messages()
        self._msg_iterator = self.get_message()
        self.verbose_level = verbose_level  # 0 means silent

    @property
    def uid(self):
        return self._uid

    @staticmethod
    @abstractmethod
    def parsable_patterns() -> List[str]:
        ...

    @staticmethod
    def is_url(text: str) -> bool:
        pattern = r"^(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$"
        return re.match(pattern, text) is not None

    @classmethod
    def get_uid_from_text(cls, txt: str) -> Optional[str]:
        txt = txt.strip()
        for pattern in cls.parsable_patterns():
            matching = re.match(pattern, txt)
            if matching is not None:
                try:
                    return matching.group('uid')
                except IndexError:
                    logger.error(f"text({txt}) matched with pattern({pattern}); but no 'uid' group name found."
                                 f"Add a group named 'uid' to the pattern.")
                    continue
        return None

    @classmethod
    def get_obj_from_text(cls, text: str, *args, **kwargs) -> Optional["BaseMessageAutomator"]:
        uid = cls.get_uid_from_text(text)
        if uid is None:
            return None
        obj = cls(uid=uid, *args, **kwargs)
        return obj

    def load_messages(self, all_message_types: bool = False) -> None:
        with open(os.path.join(BASE_DIR, 'resources', 'sample_messages.json'), 'r') as fp:
            all_messages = json.load(fp)
        if all_message_types or (not self.message_types):
            self.messages = all_messages
            return

        for key in self.message_types:
            self.messages[key] = all_messages.get(key, [])
        return

    @abstractmethod
    def prepare_payload(self, message: str) -> Dict:
        return {'msg': message}

    def _post(self, idx: int, *args) -> bool:
        payload = self.prepare_payload(next(self._msg_iterator))
        res = requests.post(
            url=self._posting_url,
            data=payload,
        )
        if self.verbose_level >= 2:
            print("{}: {} -> {}".format(idx, res.status_code, payload))
        return res.ok

    @property
    @abstractmethod
    def _posting_url(self) -> str:
        ...

    def get_message(self):
        eligible_messages = list(itertools.chain(*self.messages.values()))
        random.shuffle(eligible_messages)
        for message in itertools.cycle(eligible_messages):
            yield message

    def post(self, n: int = 1, start: int = 1) -> int:
        with ThreadPoolExecutor() as executor:
            threads = executor.map(self._post, range(1, n + 1))
        success_count = sum(threads)
        return success_count

    def spam(self, rep: int = 1) -> None:
        if not self.messages:
            self.load_messages(all_message_types=True)

        success = self.post(rep)
        if self.verbose_level >= 1:
            print(f"Success: {success}/{rep}")

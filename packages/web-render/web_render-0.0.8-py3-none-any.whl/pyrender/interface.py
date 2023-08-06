"""
Copyright 2022 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""
from dataclasses import dataclass
from typing import Union, List, Dict
import pickle
import zlib


class IBase:
    def to_dict(self) -> Dict:
        return self.__dict__


@dataclass
class MessageProtocol(IBase):
    status_code: int = 200
    payload: Union[List, Dict, None] = None
    action: str = str()
    message: str = str()


@dataclass
class IRenderData:
    html: bytes
    expiration_date: int
    status_code: int
    javascript: Union[None, int, str] = None

    @staticmethod
    def pickle_loads(data):
        return pickle.loads(data)

    @staticmethod
    def compress_zlib(data: str) -> bytes:
        return zlib.compress(data.encode("utf8"))

    def pickle_dump(self) -> bytes:
        return pickle.dumps(self)

    def decompress_field(self, name):
        if self.__dict__[name]:
            return zlib.decompress(self.__dict__[name]).decode("utf8")
        return None

    def to_dict(self):
        return {
            "html": self.decompress_field("html"),
            "javascript": self.javascript,
            "expiration_date": self.expiration_date,
            "status_code": self.status_code
        }

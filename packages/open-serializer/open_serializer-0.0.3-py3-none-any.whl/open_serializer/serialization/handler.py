from __future__ import annotations

import os as _os
from abc import ABC, abstractmethod
from typing import Union


class Serializer:
    file_handlers = {}

    @classmethod
    def register_handler(cls, name: Union[str, list[str]]) -> None:
        def wrapper(handler_cls):
            if isinstance(name, str):
                cls.file_handlers[name] = handler_cls
            elif isinstance(name, list):
                for _name in name:
                    cls.file_handlers[_name] = handler_cls
            else:
                raise TypeError(f"name must be str or list[str], not {type(name)}")

            return handler_cls

        return wrapper

    @classmethod
    def get_handler(cls, output_type):
        return cls.file_handlers[output_type]()

    @classmethod
    def auto_handler(cls, path: str) -> FileHandler:
        name = cls.get_handler_name(path)
        return cls.get_handler(name)

    @classmethod
    def get_handler_name(cls, path: str) -> str:
        return _os.path.splitext(path)[1][1:]

    @classmethod
    def serialize_object(cls, data: dict, path: str) -> None:
        handler = cls.auto_handler(path)
        handler.dump(data, path)

    @classmethod
    def deserialize_object(cls, path: str) -> dict:
        handler = cls.auto_handler(path)
        return handler.load(path)


class FileHandler(ABC):
    @abstractmethod
    def load(self, path: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    def dump(self, data: dict, path: str) -> None:
        raise NotImplementedError

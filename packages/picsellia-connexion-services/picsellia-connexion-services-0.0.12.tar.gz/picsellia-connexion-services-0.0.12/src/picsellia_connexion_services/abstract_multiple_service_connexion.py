import abc
from typing import Any


class AbstractMultipleServiceConnexion(abc.ABC):

    @abc.abstractmethod
    def get(self, key: str, path: str, data: dict = None, params: dict = None, stream=False):
        pass

    @abc.abstractmethod
    def post(self, key: str, path: str, data: dict = None, params: dict = None, files: Any = None):
        pass

    @abc.abstractmethod
    def patch(self, key: str, path: str, data: dict = None, params: dict = None):
        pass

    @abc.abstractmethod
    def put(self, key: str, path: str, data: dict = None, params: dict = None):
        pass

    @abc.abstractmethod
    def delete(self, key: str, path: str, data: dict = None, params: dict = None):
        pass
from typing import Any, Dict

from .jwt_service import JwtServiceConnexion
from .abstract_multiple_service_connexion import AbstractMultipleServiceConnexion


class MultipleJwtServiceConnexion(AbstractMultipleServiceConnexion):

    def __init__(self, host : str, base_jwt_data : dict, identifier : str) -> None:
        self.services : Dict[str, JwtServiceConnexion] = {}
        self.base_jwt_data = base_jwt_data
        self.identifier = identifier
        self.host = host
    
    def wrapped_request(f):
        def decorated(self : MultipleJwtServiceConnexion, *args, **kwargs):
            key = kwargs["key"]

            if not key in self.services:
                jwt_data = self.base_jwt_data
                jwt_data[self.identifier] = key
                self.services[key] = JwtServiceConnexion(self.host, jwt_data)

            return f(self, *args, **kwargs)

        return decorated

    def get(self, key : str, path: str, data: dict = None, params: dict = None, stream=False):
        return self.services[key].get(path, data, params, stream)
    
    def post(self, key : str, path: str, data: dict = None, params: dict = None, files: Any = None):
        return self.services[key].post(path, data, params)

    def put(self, key : str, path: str, data: dict = None, params: dict = None):
        return self.services[key].put(path, data, params)

    def delete(self, key : str, path: str, data: dict = None, params: dict = None):
        return self.services[key].delete(path, data, params)

    def patch(self, key : str, path: str, data: dict = None, params: dict = None):
        return self.services[key].delete(path, data, params)

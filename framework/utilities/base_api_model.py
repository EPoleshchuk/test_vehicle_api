from typing import Iterable
from typing import Union

from framework.api import ApiClient
from framework.consts import Consts
from project.config import ConfigData


class BaseAPIModel:
    """
    Class with Base Api Model
    """
    _API_FIELDS_MAP = None
    endpoint = None
    api_client = ApiClient(ConfigData.URL)
    update_endpoint = None

    def __init__(self, object_id: str):
        """
        Base constructor of Api Model
        :param object_id(str): object id
        """
        self.object_id = object_id

    def _update_fields(self, data: dict):
        """
        Method to update all fields after changes via api (for inner using)
        :param data(dict): Dict with Api object fields and new values
        :return: None
        :raises: ValueError if this method has not been override
        """
        raise ValueError("This method must be override")

    @classmethod
    def convert_fields(cls, data: dict, new_format: str) -> dict:
        """
        Method to convert data keys to Python or JS format using cls.FIELDS_MAP
        :param data(dict): Dict for convert
        :param new_format(str): One of (Consts.PYTHON_FORMAT, Consts.JS_FORMAT)
        :return(dict): New dict with converted keys to new_format Format
        :raises: ValueError if new_format not in (Consts.PYTHON_FORMAT, CONSTS.JS_FORMAT)
        """
        if new_format == Consts.PYTHON_FORMAT:
            return {cls._API_FIELDS_MAP[key]: data[key] for key in data}
        elif new_format == Consts.JS_FORMAT:
            return {list(cls._API_FIELDS_MAP.keys())[list(cls._API_FIELDS_MAP.values()).index(key)]: data[key]
                    for key in data}
        else:
            raise ValueError(f"Unsupported format: {new_format}")

    @classmethod
    def get_object(cls, object_id: Union[int, str, Iterable[int], Iterable[str]]):
        """
        Method to get Object by id/ids
        :param object_id(int, str, iterable): one or many object ids
        :return(cls instance(-s)): one or many instances of cls
        """
        instances = []
        if isinstance(object_id, (int, str)):
            object_id = [object_id]

        for id_ in object_id:
            response = cls.api_client.get(endpoint=f"{cls.endpoint}/{id_}").json()
            response = cls.convert_fields(response, Consts.PYTHON_FORMAT)
            instances.append(cls(**response))
        return instances[0] if len(instances) == 1 else instances

    def update_object(self, **kwargs):
        """
        Method for update object fields via POST Api request
        :param kwargs(dict): Fields to update with new values
        :return: None
        :raises: ValueError if not self.update_endpoint
        """
        if not self.update_endpoint:
            raise ValueError("This method isn't supported by this model")

        self.api_client.post(endpoint=f"{self.endpoint}/{self.object_id}/{self.update_endpoint}",
                             data=self.convert_fields(kwargs, Consts.JS_FORMAT))
        self._update_fields(kwargs)

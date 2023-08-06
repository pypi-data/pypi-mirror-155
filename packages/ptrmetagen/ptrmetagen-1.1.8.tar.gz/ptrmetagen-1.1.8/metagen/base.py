# general and helper function and classe

from typing import Union, Optional, Any, Type
from pydantic import BaseModel
from pydantic.utils import ROOT_KEY
from abc import ABC, abstractmethod
from uuid import UUID


# helper class
class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class BaseModelWithDynamicKey(BaseModel):
    """
    Pydantic workaoround for custom dynamic key
    ref: https://stackoverflow.com/questions/60089947/creating-pydantic-model-schema-with-dynamic-key
    """

    def __init__(self, **data: Any) -> None:
        if self.__custom_root_type__ and data.keys() != {ROOT_KEY}:
            data = {ROOT_KEY: data}
        super().__init__(**data)


class BaseModelArbitrary(BaseModel):
    pass

    class Config:
        arbitrary_types_allowed = True


# model classes
class LeafABC(BaseModel, ABC):
    key: Optional[UUID]

    @abstractmethod
    def __nodes__(self) -> str:
        pass

    @property
    @abstractmethod
    def hash_attrs(self) -> tuple:
        pass


def set_key_from_input(value: Union[str, UUID, Type[LeafABC]]):
    """
    Helper method used as validator in pydantic model.
    For input string, Leaf or UUID return valid UUID
    """
    if isinstance(value, LeafABC):
        return value.key
    if isinstance(value, str):
        return UUID(value)
    return value

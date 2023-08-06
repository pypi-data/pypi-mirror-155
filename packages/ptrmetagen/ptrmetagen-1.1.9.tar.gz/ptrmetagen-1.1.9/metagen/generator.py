from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, List, Type
import json

from metagen.base import LeafABC, UUIDEncoder
from metagen.helpers import create_file, open_json
from metagen.pipes import path_check
from metagen.metadata import ElementFactory, element_factory
from metagen.register import Register
from metagen.main import register, CONFIG
from metagen.importer import ImporterABC, Importer


# serialization & deserialization
class Serializer(BaseModel, ABC):

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def to_json(self, path: Union[Path, str]) -> None:
        pass


class JSONSerializer(Serializer):
    structure: dict = Field(default={})

    def to_dict(self) -> dict:
        for element in register.get_elements():
            nodes = element.__nodes__().split('.')
            self.set_node(self.structure, nodes, element)
        return self.structure

    def set_node(self, structure: dict, nodes: list, element: Type[LeafABC]):
        node = nodes.pop(0)
        if len(nodes) > 0:
            if not structure.get(node):
                structure[node] = {}
            self.set_node(structure[node], nodes, element)
        else:
            if not structure.get(node):
                structure[node] = []
            structure[node].append(element.to_dict())

    def to_json(self, path: Union[Path, str]) -> None:
        structure = self.to_dict()

        path = path_check(path)

        if not path.parent:
            create_file(path.parent)

        with open(path, 'w') as file:
            json.dump(structure, file, indent=6, cls=UUIDEncoder)


class DeSerializer(BaseModel, ABC):

    @abstractmethod
    def load(self, path: Union[Path, str], **kwargs) -> None:
        pass


class JSONDeserializer(DeSerializer):
    factory: ElementFactory = Field(default=element_factory)

    def load(self, path: Union[Path, str], encoding='utf8') -> None:

        path = path_check(path)
        obj = open_json(path, encoding)
        for node, structure in obj.items():
            self._parse(node, structure)

    def _parse(self, nodes: str, obj: Union[dict, list]) -> None:

        if isinstance(obj, dict):
            for node, structure in obj.items():
                self._parse(f'{nodes}.{node}', structure)
        elif isinstance(obj, list):
            for data in obj:
                self.factory.create_element(nodes, data)


# generator
class GeneratorABC(BaseModel, ABC):
    serializer: Serializer
    deserializer: DeSerializer
    importer: ImporterABC

    @property
    @abstractmethod
    def register(self) -> Register:
        pass

    @abstractmethod
    def import_fixtures(self) -> dict:
        pass

    class Config:
        arbitrary_types_allowed = True



class Generator(GeneratorABC):
    serializer: Serializer = Field(default=JSONSerializer())
    deserializer: DeSerializer = Field(default=JSONDeserializer())
    importer: ImporterABC = Field(default=Importer(**CONFIG.importer_setting.dict()))

    @property
    def register(self) -> Register:
        """Element Register Access """
        return register

    def import_fixtures(self) -> dict:
        return self.importer.run(self.to_dict())

    def load_fixtures(self, path: Union[Path, str], encoding='utf8') -> None:
        """Load fixtures into the register"""
        self.deserializer.load(path, encoding=encoding)

    def to_dict(self) -> dict:
        """Generate dict representation of fixtures from register"""
        return self.serializer.to_dict()

    def to_json(self, path: Union[str, Path]) -> None:
        """Generate json representation of fixtures from register"""
        self.serializer.to_json(path)

    def get_element_by_nameInternal(self, name: str) -> Type[LeafABC]:
        """Return element of given nameInternal"""
        if self.register.get_by_name(name):
            return self.register.get_by_name(name)
        else:
            raise ValueError(f'Element with nameInternal {name} did not find')

    def get_element_by_uuid(self, uuid: str) -> Type[LeafABC]:
        """Return element of given uuid"""
        if register.get_by_uuid(uuid):
            return register.get_by_uuid(uuid)
        else:
            raise ValueError(f'Element with uuid {uuid} did not find')

    def get_elements_by_type(self, element: Type[LeafABC]) -> List[Type[LeafABC]]:
        """Return list of all elements of given element type"""
        return [v for k, v in self.register.name.items() if isinstance(v, element.__wrapped__)]

    def get_elements_by_name(self, name: str) -> List[Type[LeafABC]]:
        """Return list of elements that internal name contains part of input string"""
        return [v for k, v in self.register.name.items() if k.__contains__(name)]
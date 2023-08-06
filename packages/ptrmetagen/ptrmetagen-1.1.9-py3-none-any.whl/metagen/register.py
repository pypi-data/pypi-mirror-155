from abc import ABC, abstractmethod
from uuid import UUID
from typing import Type, Any, List, Union, Dict
from warnings import warn
from pandas import DataFrame
import pandas
from pydantic import BaseModel, Field
import weakref

from metagen.base import LeafABC

# TODO: Solve weak references
# TODO: Element look up for pandas


class Register(BaseModel, ABC):

    @abstractmethod
    def get_elements(self) -> List[Type[LeafABC]]:
        pass

    @abstractmethod
    def add(self, element: Type[LeafABC]) -> None:
        pass

    @abstractmethod
    def update(self, attrName: str, value: Any)-> None:
        pass

    @abstractmethod
    def check_register(self, element: Type[LeafABC]) -> bool:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Type[LeafABC]:
        pass

    @abstractmethod
    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: UUID) -> Type[LeafABC]:
        pass

    class Config:
        arbitrary_types_allowed = True


# register
class DictRegister(Register):
    hashs: dict = Field(default_factory=dict)
    uuid: dict = Field(default_factory=dict)
    name: dict = Field(default_factory=dict)

    def get_elements(self) -> List[Type[LeafABC]]:
        return [element for element in self.hashs.values()]

    def add(self, element: Type[LeafABC]) -> None:
        if not self.check_register(element):
            self.hashs.update({hash(element): element})
            self.uuid.update({str(element.key): element})
            self.name.update({element.nameInternal: element})
        else:
            raise ValueError(f'PTR element "{element.__class__.__name__}" with nameInternal: {element.nameInternal}, '
                             f'key: {element.key} and hash: {hash(element)} already exist')

    def update(self, attrName: str, value: Any)-> None:
        raise NotImplementedError()

    def check_register(self, element: Type[LeafABC]) -> bool:
        return all([self.hashs.get(hash(element)), self.name.get(element.nameInternal)])

    def get_by_name(self, name: str) -> Type[LeafABC]:
        return self.name.get(name)

    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        return self.hashs.get(hash)

    def get_by_uuid(self, uuid: str) -> Type[LeafABC]:
        if UUID(uuid):
            return self.uuid.get(uuid)


def prepare_element4pandas(element: Type[LeafABC]) -> dict:
    """Helper function, creates dict for allement to concat later the element dict into pandas dataframe"""
    element_dict = {k:v for k, v in element.dict().items() if not isinstance(v, (list, dict, tuple))}
    element_dict['element'] = weakref.ref(element)
    element_dict['type'] = element.__class__.__name__
    element_dict['hash'] = hash(element)
    return element_dict


class PandasRegister(Register):
    table: DataFrame = Field(default_factory=DataFrame)
    element_instances: list = Field(default_factory=list)

    def get_elements(self) -> List[Type[LeafABC]]:
        return [element() for element in self.table['element'].values]

    def add(self, element: Type[LeafABC]) -> None:
        """Add element to register. If element hash in register rise error"""
        self.element_instances.append(element)
        element_pd = DataFrame(prepare_element4pandas(element), index=['key'])
        self.table = pandas.concat([self.table, element_pd], ignore_index=True, axis=0)

    def update(self, attrName: str, value: Any):
        raise NotImplementedError()

    def check_register(self, element: Type[LeafABC])-> bool:
            if self.get_by_hash(hash(element)):
                return True
            else:
                return False

    def get_by_name(self, name: str) -> Type[LeafABC]:
        return self.get_by_attrName(name, attrName='nameInternal')

    def get_by_hash(self, hash: int) -> Type[LeafABC]:
        return self.get_by_attrName(hash, attrName='hash')

    def get_by_uuid(self, uuid: UUID) -> Type[LeafABC]:
        return self.get_by_attrName(uuid, attrName='key')

    def get_by_attrName(self, value: Any, attrName: str) -> Union[None, Type[LeafABC]]:
        """Find element in register based on columne name and ist value """
        try:
            filter = self.table[attrName] == value
        except KeyError:
            return None

        if not any(value for value in filter.values):
            warn(f'No element found for attrName: {attrName} and value {value}')
            return None
        return self.table.loc[filter]['element'].item()()


class RegisterFactory(BaseModel):
    registers: Dict[str, Type[Register]] = Field(default_factory=dict)

    def add(self, registerName: str, registerType: Type[Register]) -> None:
        self.registers.update({registerName: registerType})

    def get(self, registerName: str, **ignore) -> Type[Register]:
        return self.registers[registerName]


register_factory = RegisterFactory()
register_factory.add(registerName='dict', registerType=DictRegister)
register_factory.add(registerName='pandas', registerType=PandasRegister)

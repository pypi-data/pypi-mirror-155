import json
from abc import ABC
from pathlib import Path
from typing import Union, Any, Callable
from uuid import UUID
import copy
from functools import wraps
from warnings import warn
from dataclasses import dataclass, field

from metagen.main import register


# helpe class to define and create pipileines
@dataclass
class Process(ABC):
    """Abstrac factory for processes"""

    @classmethod
    def __call__(self, *args, **kwargs):
        pass


class PipeMeta(type):
    def __new__(cls, clsname: str, superclasses: tuple, clsdict: dict):
        stac = [value for attr, value in clsdict.items() if (isinstance(value, (Process, Callable)))
                and (not attr.__contains__('__'))]
        clsdict.update(stac=stac)
        return super().__new__(cls, clsname, superclasses, clsdict)


class Pipe(metaclass=PipeMeta):

    def __call__(self, value) -> Any:
        current = value
        for method in self.stac:
            current = method(current)
        return current

# helper functions
def create_file(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def str2Path(path: Union[Path, str]) -> Path:
    if not isinstance(path, Path):
        return Path(path)
    return path


def is_exist(obj: Any) -> Any:
    if not hasattr(obj, 'exists'):
        raise AttributeError(f'Object {obj} has not method ')
    if not obj.exists():
        raise ValueError(f'{obj} does not exist')
    return obj


def prepare_data_for_leaf(obj: dict) -> dict:
    new = obj.copy()
    data = new.pop('data')
    new.update(data)
    return new


def open_json(path: Union[str, Path], encoding='utf8'):
    with open(path, 'r', encoding=encoding) as file:
        return json.load(file)


# TODO: not used, need to be implemented hash_attr, currently not used
def make_hash(o):
    """ Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries). """

    if isinstance(o, (set, tuple, list)):
        return tuple([make_hash(e) for e in o])

    elif not isinstance(o, dict):

        return hash(o)

    new_o = copy.deepcopy(o)
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))


# helpers dacoratoes
def exist_in_register(element):
    @wraps(element)
    def checking_register(*args, **kwargs):
        instance = element(*args, **kwargs)
        if register.check_register(instance):
            registered_element = register.get_by_hash(hash(instance))
            warn(f'Element duplication: Element {instance.__class__.__name__} with parameters: '
                 f'{"; ".join([f"{k}: {v}" for k, v in kwargs.items()])} found in register. Element '
                 f'{registered_element.__repr__()} returned instead')
            return registered_element
        else:
            register.add(instance)
            return instance
    return checking_register
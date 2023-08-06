from pydantic import BaseModel, Field, HttpUrl
import yaml
from typing import Literal, Optional
from pathlib import Path

BASE_CONFIG_FILE = Path(__file__).parent / 'config.yaml'


class Register(BaseModel):
    registerName: Literal['pandas', 'dict']


class Importer(BaseModel):
    path: Optional[Path]
    instance_url: Optional[HttpUrl]


class Config(BaseModel):
    register_setting: Register = Field(default_factory=Register)
    importer_setting: Importer = Field(default_factory=Importer)


def load_yaml(path: str) -> Config:
    with open(path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def dump_yaml(path: Path, data: dict) -> None:
    with open(path, 'w') as file:
        file.write(yaml.dump(data, Dumper=yaml.Dumper))



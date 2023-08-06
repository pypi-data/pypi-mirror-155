from dataclasses import dataclass
from typing import Optional, List, Union


@dataclass
class BaseEnv:
    base_docker_image: str


@dataclass
class AuxEnv:
    name: str
    conda_yaml: str
    local_modules_paths: List[str]


Env = Union[BaseEnv, AuxEnv]
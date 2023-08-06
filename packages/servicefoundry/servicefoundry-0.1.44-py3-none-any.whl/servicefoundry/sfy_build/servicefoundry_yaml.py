from os.path import exists
from typing import Dict

import yaml
from pydantic import BaseModel

from servicefoundry.sfy_build.const import SERVICEFOUNDRY_YAML


class BuildPack(BaseModel):
    build_pack: str
    options: Dict[str, str]


class ServiceFoundryYaml(BaseModel):

    name: str
    build: BuildPack

    @classmethod
    def create(cls, sfy_yaml=SERVICEFOUNDRY_YAML):
        if exists(sfy_yaml):
            with open(sfy_yaml, "r") as file:
                yaml_parsed = yaml.safe_load(file)
                # @TODO Verify json schema using pydantic
                return cls(**yaml_parsed)

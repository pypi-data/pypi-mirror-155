from typing import List, Union

from servicefoundry.internal.const import KIND
from servicefoundry.internal.exceptions import ConfigurationException

STRING = "string"
NUMBER = "number"
OPTIONS = "options"
WORKSPACE = "tfy-workspace"
FILE = "tfy-file"
PYTHON_FILE = "tfy-python-file"

default = Union[str, int, float, None]


class TemplateParameter:
    id: str
    kind: str
    prompt: str
    default: default
    suggest: default

    def __init__(self, json_def):
        self.id = json_def["id"]
        self.kind = json_def["kind"]
        self.prompt = json_def["prompt"]
        if "default" in json_def:
            self.default = json_def["default"]
        else:
            self.default = None
        if "suggest" in json_def:
            self.suggest = json_def["suggest"]
        else:
            self.suggest = ""


class OptionsTemplateParameter(TemplateParameter):
    options: List[str]

    def __init__(self, json_def):
        super().__init__(json_def)
        self.options = json_def[OPTIONS]


def _get_workspace_choices(client):
    spaces = client.list_workspace()
    space_choices = [
        (space["name"], space["fqn"])
        for space in spaces
        if space["status"] == "CREATE_SPACE_SUCCEEDED"
    ]
    return space_choices


class WorkspaceTemplateParameter(TemplateParameter):
    def __init__(self, json_def):
        super().__init__(json_def)

    def get_workspaces(self, client):
        return _get_workspace_choices(client)


def get_template_parameter(parameter):
    kind = parameter[KIND]
    if kind in [STRING, NUMBER, FILE, PYTHON_FILE]:
        return TemplateParameter(parameter)
    if kind == OPTIONS:
        return OptionsTemplateParameter(parameter)
    if kind == WORKSPACE:
        return WorkspaceTemplateParameter(parameter)
    raise ConfigurationException(f"Unhandled template parameter kind '{kind}'")

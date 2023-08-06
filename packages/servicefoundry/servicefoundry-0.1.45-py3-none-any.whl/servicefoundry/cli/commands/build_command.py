import logging

import rich_click as click

from servicefoundry.cli.const import GROUP_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.sfy_build.build import build

logger = logging.getLogger(__name__)


def _build(name):
    build(name)


@click.group(
    name="build",
    cls=GROUP_CLS,
    invoke_without_command=True,
    help="Build servicefoundry Service",
)
@click.option("--name", type=click.STRING, default=None)
@handle_exception_wrapper
def build_command(name):
    _build(name)


def get_build_command():
    return build_command

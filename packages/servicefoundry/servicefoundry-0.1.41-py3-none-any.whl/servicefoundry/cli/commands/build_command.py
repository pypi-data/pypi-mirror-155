import logging

import rich_click as click

from servicefoundry.cli.const import GROUP_CLS
from servicefoundry.cli.util import handle_exception_wrapper
from servicefoundry.sfy_build.build import build

logger = logging.getLogger(__name__)


def _build():
    build()


@click.group(
    name="build",
    cls=GROUP_CLS,
    invoke_without_command=True,
    help="Build servicefoundry Service",
)
@handle_exception_wrapper
def build_command():
    _build()


def get_build_command():
    return build_command

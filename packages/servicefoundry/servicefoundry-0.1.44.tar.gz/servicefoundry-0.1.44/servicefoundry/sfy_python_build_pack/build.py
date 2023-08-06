from os.path import join

from servicefoundry.sfy_build_pack_common.docker_util import build_docker
from servicefoundry.sfy_build_pack_common.file_util import write_file
from servicefoundry.sfy_python_build_pack.docker_file import (
    PYTHON_39,
    BaseDockerFile,
    Honcho,
    Requirements,
)


def generate_docker_file():
    return BaseDockerFile(
        layers=[Requirements(), Honcho()], base_image=PYTHON_39
    ).to_dockerfile()


def build(name, build_dir, **kwargs):
    docker_file_str = generate_docker_file()
    docker_file = join(build_dir, "Dockerfile")
    write_file(docker_file, docker_file_str)
    build_docker(name, docker_file_path=docker_file)

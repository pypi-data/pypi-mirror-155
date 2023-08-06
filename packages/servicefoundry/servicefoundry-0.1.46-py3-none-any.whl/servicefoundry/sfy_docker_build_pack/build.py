from servicefoundry.sfy_build_pack_common.docker_util import build_docker


def build(name, **kwargs):
    build_docker(name)

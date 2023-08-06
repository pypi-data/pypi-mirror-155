import os
import sys
import traceback

from servicefoundry.sfy_build.build_pack import detect_build_pack, get_build_pack
from servicefoundry.sfy_build.const import BUILD_DIR
from servicefoundry.sfy_build.servicefoundry_yaml import ServiceFoundryYaml
from servicefoundry.sfy_build_pack_common.file_util import create_dir


def build():
    sfy_yaml = ServiceFoundryYaml.create()
    if sfy_yaml:
        name = sfy_yaml.name
    else:
        name = os.path.basename(os.getcwd())

    options = None
    if sfy_yaml and sfy_yaml.build and sfy_yaml.build.build_pack:
        build_pack = get_build_pack(sfy_yaml.build.build_pack)
        if sfy_yaml.build.options:
            options = sfy_yaml.build.options
    else:
        build_pack = detect_build_pack()
        if build_pack is None:
            print("No build pack configured to build this package.")
            sys.exit(1)

    print(f"Going to use build pack {build_pack.name}")
    create_dir(BUILD_DIR)
    build_pack.build(name=name, build_dir=BUILD_DIR, options=options)
    print(f"Created docker image {name}.")


def main():
    try:
        return build()
    except Exception as e:
        traceback.print_exc()
        raise e


if __name__ == "__main__":
    main()

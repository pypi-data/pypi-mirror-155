import importlib


class BuildPack:
    def __init__(self, name, detect, build):
        self.name = name
        self._detect = detect
        self._build = build

    def detect(self):
        return self._detect()

    def build(self, name, build_dir, options):
        return self._build(name=name, build_dir=build_dir, options=options)


def _get_build_pack(module_name):
    def _build_pack():
        try:
            detect_module = importlib.import_module(f"{module_name}.detect")
            build_module = importlib.import_module(f"{module_name}.build")
            return BuildPack(module_name, detect_module.detect, build_module.build)
        except Exception as e:
            print(f"Failed to load {module_name} because of exception: {str(e)}")
            return None

    return _build_pack


_build_pack_provider_chain = {
    "sfy_docker_build_pack": _get_build_pack("servicefoundry.sfy_docker_build_pack"),
    "sfy_python_build_pack": _get_build_pack("servicefoundry.sfy_python_build_pack"),
    "sfy_fallback_build_pack": _get_build_pack(
        "servicefoundry.sfy_fallback_build_pack"
    ),
}


def get_build_pack(name: str):
    return _build_pack_provider_chain[name]()


def detect_build_pack():
    final_build_pack = None
    for build_pack_provider in _build_pack_provider_chain.values():
        build_pack = build_pack_provider()
        if build_pack is not None:
            if build_pack.detect():
                print(f"Build pack {build_pack.name} can build this package.")
                if final_build_pack is None:
                    final_build_pack = build_pack
            else:
                print(f"Build pack {build_pack.name} can't build this package.")
    return final_build_pack

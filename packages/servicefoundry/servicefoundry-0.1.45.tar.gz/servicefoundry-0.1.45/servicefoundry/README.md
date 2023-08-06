## Note
* Don't create cross dependency between build pack.
Keep all the common logic in `sfy_build_pack_common`

## sfy_build

This module is executed when `sfy build` is executed.
This module take care of converting code to docker image.

This package runs all the build_pack in a chain.
New build pack can be added in chain at [build_pack.py](sfy_build/build_pack.py)

All the build pack must have `detect.py` and `build.py`.

Example `build.py`:
```python
def build(name, build_dir, **kwargs):
    pass
```

Example `detect.py`:
```python
def detect(**kwargs):
    pass
```


## sfy_build_pack_common

This module has utilities which is used by build packs.

## sfy_docker_build_pack

This build pack will build if there is Dockerfile

## sfy_python_build_pack

This build pack will build if there is `requirements.txt` and `Procfile`

## sfy_fallback_build_pack

This build pack will try building everything else using 3rd party build packs.

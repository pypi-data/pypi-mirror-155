from servicefoundry.sfy_python_build_pack.docker_file.layer import Layer


class Requirements(Layer):
    def build(self):
        return "\n".join(
            [
                "COPY requirements.txt requirements.txt",
                "RUN pip install --no-cache-dir --upgrade -r requirements.txt",
            ]
        )

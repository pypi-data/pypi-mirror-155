import os


def detect(**kwargs):
    if os.path.isfile("Dockerfile"):
        return True
    return False

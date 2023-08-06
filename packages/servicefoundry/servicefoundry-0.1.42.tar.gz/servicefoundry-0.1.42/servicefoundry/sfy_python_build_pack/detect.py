import os


def detect(**kwargs):
    if os.path.isfile("requirements.txt"):
        if os.path.isfile("Procfile"):
            return True
        print(f"Found requirements.txt file, but can't find Procfile.")
    return False

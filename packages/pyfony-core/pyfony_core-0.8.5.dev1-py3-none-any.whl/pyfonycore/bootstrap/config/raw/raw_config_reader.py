from pathlib import Path
from pyfonycore import pyproject


def is_defined(raw_config):
    return "pyfony" in raw_config and "bootstrap" in raw_config["pyfony"]


def read(pyproject_path: Path):
    config = pyproject.read(pyproject_path)
    return get_boostrap_config(config)


def get_boostrap_config(raw_config):
    if "pyfony" not in raw_config:
        raise Exception("[pyfony] section is missing in pyproject.toml")

    if "bootstrap" not in raw_config["pyfony"]:
        raise Exception("[pyfony.bootstrap] section is missing in pyproject.toml")

    return raw_config["pyfony"]["bootstrap"]

import os
from pathlib import Path
import tomlkit
from tomlkit.toml_document import TOMLDocument


def read(pyproject_path: Path) -> TOMLDocument:
    with pyproject_path.open("r", encoding="utf-8") as t:
        return tomlkit.parse(t.read())


def get_path(working_dir=os.getcwd()):
    return Path(working_dir).joinpath("pyproject.toml")

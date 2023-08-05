from pyfonycore import pyproject
from pyfonycore.bootstrap.config import config_factory
from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.bootstrap.config.raw import raw_config_reader


def read() -> Config:
    raw_config = raw_config_reader.read(pyproject.get_path())
    return config_factory.create(raw_config, "[pyfony.bootstrap]")

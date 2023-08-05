from injecta.module import attribute_loader
from pyfonycore.Kernel import Kernel


def resolve(raw_config):
    return attribute_loader.load(*raw_config["kernel_class"].split(":")) if "kernel_class" in raw_config else Kernel

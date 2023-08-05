from pyfonycore.bootstrap.config.Config import Config
from pyfonycore.bootstrap.config.raw import (
    container_init_resolver,
    root_module_name_resolver,
    allowed_environments_resolver,
    kernel_class_resolver,
)


def create(raw_config, pyproject_source: str):
    if container_init_resolver.container_init_defined(raw_config):
        init_container = container_init_resolver.resolve(raw_config, pyproject_source)
    else:
        from pyfonycore.container.container_init import init as init_container

    return Config(
        init_container,
        kernel_class_resolver.resolve(raw_config),
        root_module_name_resolver.resolve(raw_config),
        allowed_environments_resolver.resolve(raw_config),
    )

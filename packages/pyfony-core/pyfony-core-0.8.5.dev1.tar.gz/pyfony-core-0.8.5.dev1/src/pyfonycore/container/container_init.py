from typing import List
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.path_resolver import resolve_path
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import pyfony_bundles_loader
from pyfonycore.bootstrap.config.Config import Config


def init(app_env: str, bootstrap_config: Config) -> ContainerInterface:
    bundles = pyfony_bundles_loader.load_bundles()
    kernel = create_kernel(app_env, bootstrap_config, bundles)

    return kernel.init_container()


def init_with_current_bundle(app_env: str, bootstrap_config: Config) -> ContainerInterface:
    bundles = pyfony_bundles_loader.load_bundles_with_current()
    kernel = create_kernel(app_env, bootstrap_config, bundles)

    return kernel.init_container()


def create_kernel(app_env: str, bootstrap_config: Config, bundles: List[Bundle]):
    kernel = bootstrap_config.kernel_class(
        app_env,
        resolve_path(bootstrap_config.root_module_name) + "/_config",
        YamlConfigReader(),
        bundles,
    )
    kernel.set_allowed_environments(bootstrap_config.allowed_environments)

    return kernel

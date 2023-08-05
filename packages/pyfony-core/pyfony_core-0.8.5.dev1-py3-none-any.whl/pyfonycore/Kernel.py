import os
from typing import List
from injecta.config.ConfigReaderInterface import ConfigReaderInterface
from injecta.container.ContainerBuild import ContainerBuild
from injecta.container.ContainerBuilder import ContainerBuilder
from injecta.container.ContainerInitializer import ContainerInitializer
from injecta.container.ContainerInterface import ContainerInterface
from pyfonybundles.Bundle import Bundle
from pyfonycore.container.PyfonyHook import PyfonyHooks


class Kernel:

    _allowed_environments = ["dev", "test", "prod"]

    def __init__(
        self,
        app_env: str,
        config_dir: str,
        config_reader: ConfigReaderInterface,
        bundles: List[Bundle] = None,
    ):
        self._app_env = app_env
        self._config_dir = config_dir
        self._config_reader = config_reader
        self._bundles = bundles or []
        self._container_builder = ContainerBuilder()

    def set_allowed_environments(self, allowed_environments: list):
        self._allowed_environments = allowed_environments

    def init_container(self) -> ContainerInterface:
        if self._app_env not in self._allowed_environments:
            raise Exception(f"Unexpected environment: {self._app_env}")

        hooks = self._create_pyfony_hooks()
        return self._init_container_from_hooks(hooks)

    def _read_config(self):
        return self._config_reader.read(self._get_config_path())

    def _init_container_from_hooks(self, hooks: PyfonyHooks):
        config = self._read_config()
        container_build = self._container_builder.build(config, hooks)
        return self._init_and_boot_container(container_build)

    def _create_pyfony_hooks(self):
        return PyfonyHooks(self._bundles, self._get_config_path(), self._get_project_bundles_config_dir(), self._app_env)

    def _init_and_boot_container(self, container_build: ContainerBuild):
        container = ContainerInitializer().init(container_build)
        self._boot(container)

        return container

    def _get_config_path(self):
        return f"{self._config_dir}/config_{self._app_env}.yaml"

    def _get_project_bundles_config_dir(self):
        return os.path.dirname(self._get_config_path()) + "/bundles"

    def _boot(self, container: ContainerInterface):
        for bundle in self._bundles:
            bundle.boot(container)

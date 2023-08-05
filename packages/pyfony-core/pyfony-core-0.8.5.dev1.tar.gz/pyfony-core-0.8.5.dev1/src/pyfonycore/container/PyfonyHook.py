import os
from typing import List, Tuple
from box import Box
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from injecta.config.ConfigMerger import ConfigMerger
from injecta.container.ContainerBuild import ContainerBuild
from injecta.container.Hooks import Hooks
from injecta.service.Service import Service
from injecta.service.ServiceAlias import ServiceAlias
from pyfonybundles.Bundle import Bundle
from pyfonybundles.BundleManager import BundleManager


class PyfonyHooks(Hooks):
    def __init__(self, bundles: List[Bundle], config_path: str, project_bundles_config_dir: str, app_env: str):
        self.__config_merger = ConfigMerger()
        self.__bundle_manager = BundleManager(bundles)
        self.__config_path = config_path
        self.__project_bundles_config_dir = project_bundles_config_dir
        self.__app_env = app_env

    def start(self, raw_config: dict) -> dict:
        bundles_config = self.__bundle_manager.get_bundles_config()
        project_bundles_config = self.__bundle_manager.get_project_bundles_config(self.__project_bundles_config_dir)

        raw_config = self.__config_merger.merge(self.__config_merger.merge(bundles_config, project_bundles_config), raw_config)

        return self.__bundle_manager.modify_raw_config(raw_config)

    def services_prepared(
        self, services: List[Service], aliases: List[ServiceAlias], parameters: Box
    ) -> Tuple[List[Service], List[ServiceAlias]]:
        return self.__bundle_manager.modify_services(services, aliases, parameters)

    def get_custom_parameters(self) -> dict:
        pyfony_custom_parameters = {
            "project": {
                "config_dir": os.path.dirname(self.__config_path),
            },
            "kernel": {
                "environment": self.__app_env,
            },
        }

        return self.__config_merger.merge(super().get_custom_parameters(), pyfony_custom_parameters, False)

    def parameters_parsed(self, parameters: Box) -> Box:
        return self.__bundle_manager.modify_parameters(parameters)

    def container_build_ready(self, container_build: ContainerBuild):
        for compiler_pass in self.__bundle_manager.get_compiler_passes():  # type: CompilerPassInterface
            compiler_pass.process(container_build)

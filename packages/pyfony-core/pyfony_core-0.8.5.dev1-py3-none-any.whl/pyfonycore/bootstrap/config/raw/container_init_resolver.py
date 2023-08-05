from injecta.module import attribute_loader


def container_init_defined(raw_config):
    return "container_init" in raw_config


def resolve(raw_config, pyproject_source: str):
    container_init_function_spec = get_container_init(raw_config, pyproject_source)
    return attribute_loader.load(*container_init_function_spec)


def get_container_init(raw_config: dict, pyproject_source: str):
    if "container_init" not in raw_config:
        raise Exception(f"container_init is missing in {pyproject_source} in pyproject.toml")

    return raw_config["container_init"].split(":")

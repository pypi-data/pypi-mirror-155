import os


def resolve(raw_config):
    if "root_module_name" in raw_config:
        return raw_config["root_module_name"]

    root_module_name_search_exclude = _get_root_module_name_search_exclude(raw_config)

    return _resolve_root_module_name(root_module_name_search_exclude)


def _unify_module_name(name: str):
    if name.endswith(".py"):
        return name[:-3]

    return name


def _get_root_module_name_search_exclude(raw_config):
    root_module_name_search_exclude = (
        raw_config["root_module_name_search_exclude"] if "root_module_name_search_exclude" in raw_config else []
    )
    root_module_name_search_exclude = [_unify_module_name(item) for item in root_module_name_search_exclude]

    return root_module_name_search_exclude


def _resolve_root_module_name(root_module_name_search_exclude: list):
    root_module_name_search_exclude.append("__pycache__")

    root_modules = [_unify_module_name(module_name) for module_name in os.listdir(f"{os.getcwd()}/src")]
    root_modules = [root_module for root_module in root_modules if root_module not in root_module_name_search_exclude]

    if len(root_modules) != 1:
        raise Exception(f"Cannot resolve root module from 'src' folder, it must contain exactly 1 root module, found: {root_modules}")

    return root_modules[0]

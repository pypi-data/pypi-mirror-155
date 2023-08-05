from pyfonycore.bootstrap.config import config_reader


def init(app_env: str):
    bootstrap_config = config_reader.read()
    return bootstrap_config.container_init_function(app_env, bootstrap_config)

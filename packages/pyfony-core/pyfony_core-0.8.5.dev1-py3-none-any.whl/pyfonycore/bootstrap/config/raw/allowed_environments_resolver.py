def resolve(raw_config):
    return raw_config["allowed_environments"] if "allowed_environments" in raw_config else ["dev", "test", "prod"]

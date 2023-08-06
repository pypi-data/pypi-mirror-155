import abc
import os

USER_HOME_DIR = os.path.expanduser("~")
ARCHIMEDES_CONF_DIR = os.path.join(USER_HOME_DIR, ".archimedes")

if not os.path.exists(ARCHIMEDES_CONF_DIR):
    os.mkdir(ARCHIMEDES_CONF_DIR)

ARCHIMEDES_API_CONFIG = {
    "prod": {
        "client_id": "5bc3a702-d753-43ff-9051-e7fdfdd95023",
        "aad_app_client_id": "c0a9f773-6276-4d71-8df6-7239e695aff6",
        "url": "https://api.fabapps.io",
        "authority": "https://login.microsoftonline.com/common",
    },
    "dev": {
        "client_id": "2e2f3c84-d1aa-49cc-90a2-fd3fa3380d27",
        "aad_app_client_id": "eaaa9f9f-395d-46aa-847f-b5fb6c087ff6",
        "url": "https://api-dev.fabapps.io",
        "authority": "https://login.microsoftonline.com/common",
    },
}


class InvalidEnvironmentException(Exception):
    pass


class ApiConfig(abc.ABC):
    def __init__(self, env):
        self.config = ARCHIMEDES_API_CONFIG
        if env not in self.config.keys():
            raise InvalidEnvironmentException(
                f"Invalid environment {env}, "
                f"supported values are {', '.join([str(key) for key in self.config.keys()])}"
            )
        self.environment = env.lower()

    def __getattr__(self, item):
        env_config = self.config[self.environment]
        return env_config[item]


def get_api_config(environment):
    return ApiConfig(environment)


def get_config_path(env):
    return os.path.join(ARCHIMEDES_CONF_DIR, f"arcl-{env}.json")


def get_token_path(env):
    return os.path.join(ARCHIMEDES_CONF_DIR, f"msal-{env}.cache.bin")


def get_legacy_config_path():
    return os.path.join(ARCHIMEDES_CONF_DIR, f"arcl.json")


def get_legacy_token_path():
    return os.path.join(ARCHIMEDES_CONF_DIR, f"msal.cache.bin")

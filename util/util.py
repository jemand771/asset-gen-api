import os

from .types import ConfigurationError


def get_env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise ConfigurationError

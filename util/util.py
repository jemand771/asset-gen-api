import os

from .types import ConfigurationError, MediaType


def get_env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise ConfigurationError


def preprocess_string(input_str, target_type):
    if target_type == MediaType.integer:
        # TODO handle type errors
        return int(input_str)
    return input_str

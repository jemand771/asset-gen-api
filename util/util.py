import os

from .types import ConfigurationError, InvalidInputError, MediaType


def get_env(name):
    try:
        return os.environ[name]
    except KeyError:
        raise ConfigurationError


def preprocess_string(input_str, target_type):
    if target_type == MediaType.integer:
        try:
            return int(input_str)
        except ValueError:
            raise InvalidInputError(f"'{input_str}' is not an integer")
    if target_type == MediaType.boolean:
        if input_str.lower() in ("true", "yes", "on", "1"):
            return True
        if input_str.lower() in ("false", "no", "off", "0"):
            return False
        raise InvalidInputError("unknown value for boolean")
    return input_str

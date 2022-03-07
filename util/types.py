import functools
from enum import Enum, auto


class MediaType(Enum):
    text = auto()
    image = auto()


class AllHandlerBase:
    allow_cache = False  # TODO enable and test me

    def __init__(self):
        if self.allow_cache:
            self.run = functools.cache(self.run)

    def run(self, *args, **kwargs):
        pass


class GeneratorBase(AllHandlerBase):
    input_params: dict
    name: str = None
    output_type: MediaType


class InputBase(AllHandlerBase):
    name: str = None
    params: dict
    type: MediaType


class OutputBase(AllHandlerBase):
    allow_cache = False
    name: str = None
    type: MediaType


class ConfigurationError(KeyError):
    pass

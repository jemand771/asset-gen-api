import functools
from enum import Enum, auto

from PIL import Image


class MediaType(Enum):
    text = auto()
    image = auto()
    integer = auto()


def copy_if_image(arg):
    if isinstance(arg, Image.Image):
        return arg.copy()
    return arg


def image_copier(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*[copy_if_image(x) for x in args], **{key: copy_if_image(value) for key, value in kwargs.items()})

    return wrapper


class AllHandlerBase:
    allow_cache = True

    def __init__(self):
        if self.allow_cache:
            self.run = functools.cache(self.run)
        self.run = image_copier(self.run)

    def run(self, *args, **kwargs):
        pass


class GeneratorBase(AllHandlerBase):
    input_params: dict
    name: str = None
    output_type: MediaType


class OutputBase(AllHandlerBase):
    allow_cache = False
    name: str = None
    type: MediaType


class ConfigurationError(KeyError):
    pass

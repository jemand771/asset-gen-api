import functools
from dataclasses import dataclass
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


@dataclass
class Runner:
    generator: type(GeneratorBase)
    args: dict[str, any]

    def __init__(self, generator, **kwargs):
        self.generator = generator
        self.args = kwargs

    def run(self, input_params):
        # TODO generator registry?
        return self.generator().run(
            **{
                name: (
                    value.run(input_params) if isinstance(value, Runner) else
                    value.get(input_params) if isinstance(value, MappedParam) else
                    value
                )
                for name, value in self.args.items()
            }
        )


# TODO represent this as a generator?
@dataclass
class MappedParam:
    name: str = None
    func = None

    def get(self, input_params):
        target = input_params if self.name is None else input_params[self.name]
        return target if self.func is None else self.func(target)


class GeneratorChain(GeneratorBase):
    chain: Runner

    def run(self, *args, **kwargs):
        return self.chain.run(kwargs)

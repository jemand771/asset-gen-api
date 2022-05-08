import functools
from dataclasses import dataclass
from enum import Enum, auto

from PIL import Image

from . import loader
from . import metrics


class MissingArgumentError(KeyError):
    pass


class InvalidInputError(ValueError):
    pass


class GeneratorInternalError(RuntimeError):
    pass


class GeneratorNotFoundError(ValueError):
    pass


class MediaType(Enum):
    text = auto()
    image = auto()
    integer = auto()
    box = auto()
    boolean = auto()
    color = auto()
    font = auto()


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
    name: str = None
    type: MediaType

    def __init__(self):
        if self.allow_cache:
            self.run = functools.cache(self.run)
            metrics.add_run_cache_stats(self.run, self.name)
        self.run = image_copier(self.run)

    def run(self, *args, **kwargs):
        pass


class GeneratorBase(AllHandlerBase):
    input_params: dict


class OutputBase(AllHandlerBase):
    allow_cache = False


class ConfigurationError(KeyError):
    pass


# TODO can this be cached?
@dataclass
class Runner:
    generator: type(GeneratorBase)
    args: dict[str, any]

    def __init__(self, generator, **kwargs):
        self.generator = generator
        self.args = kwargs

    def run(self, input_params):
        return loader.registry.find_generator_by_class(self.generator).run(
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


@dataclass
class Box:
    x1: int
    x2: int
    y1: int
    y2: int

    @classmethod
    def from_xywh(cls, x, y, w, h):
        return cls(x1=x, y1=y, x2=x + w, y2=y + h)

    @classmethod
    def from_xy_wh(cls, xy, wh):
        return cls.from_xywh(*xy, *wh)

    @classmethod
    def from_xyxy(cls, x1, y1, x2, y2):
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)

    @classmethod
    def from_xy_xy(cls, p1, p2):
        return cls.from_xyxy(*p1, *p2)

    @property
    def p1(self):
        return self.x1, self.y1

    @property
    def p2(self):
        return self.x2, self.y2

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1

    @property
    def dim(self):
        return self.width, self.height

    @property
    def xyxy(self):
        return *self.p1, *self.p2

    @property
    def ratio(self):
        return self.width / self.height

    @property
    def iratio(self):
        return self.height / self.width

    @property
    def whbox(self):
        return Box.from_xy_wh((0, 0), self.dim)

    def __hash__(self):
        return self.xyxy.__hash__()

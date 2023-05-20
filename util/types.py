import functools
from dataclasses import dataclass
from typing import Any

from PIL import Image

from . import metrics


class InvalidInputError(ValueError):
    pass


class GeneratorInternalError(RuntimeError):
    pass


def copy_if_image(arg):
    if isinstance(arg, Image.Image):
        return arg.copy()
    return arg


def image_copier(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*[copy_if_image(x) for x in args], **{key: copy_if_image(value) for key, value in kwargs.items()})

    return wrapper


class GeneratorBase:
    allow_cache = True
    type: str

    def __init__(self):
        if self.allow_cache:
            self.run = functools.cache(self.run)
            metrics.add_run_cache_stats(self.type, self.run.cache_info)
        self.run = image_copier(self.run)

    def run(self, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        pass


class ConfigurationError(KeyError):
    pass


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

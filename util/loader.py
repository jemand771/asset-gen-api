import importlib.util
import inspect
from pathlib import Path

from util.graph import Graph
from util.types import GeneratorBase


class Registry:
    def __init__(self):
        self.generators = {}
        self.presets = {}

    def load_generators(self):
        self.generators = self.load_classes(Path("generators"), "generators", GeneratorBase)

    def load_presets(self):
        self.presets = self.load_classes(Path("presets"), "presets", Graph)

    @staticmethod
    def load_classes(folder: Path, module_prefix, base_class, excluded_classes=None):
        if excluded_classes is None:
            excluded_classes = []
        excluded_classes.append(base_class)
        classes = []
        for file in folder.glob("**/*.py"):
            # TODO clean up module name calculation (support subdirs)
            spec = importlib.util.spec_from_file_location(module_prefix + "." + file.stem, file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except ImportError:
                print("warning: failed to immport", file)
                continue
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, base_class) and obj not in excluded_classes:
                    classes.append(obj)
        instances = {}
        for class_ in classes:
            # noinspection PyBroadException
            try:
                instances[class_.type] = class_()
            except Exception:
                print(f"failed to init {class_}")
        return instances

    def find_generator(self, name):
        return self.generators[name]


registry = Registry()
# this runs on import which is fine because... well, we _are_ importing stuff
registry.load_generators()
registry.load_presets()


def patch_image_hashable():
    from PIL.PngImagePlugin import PngImageFile
    from PIL.Image import Image

    def __hash__(self):
        import hashlib
        return int(hashlib.md5(self.tobytes()).hexdigest(), 16)

    PngImageFile.__hash__ = __hash__
    Image.__hash__ = __hash__

import importlib.util
import inspect
from pathlib import Path
from util.types import InputBase, GeneratorBase, OutputBase


def load_classes(folder: Path, base_class):
    classes = []
    for file in folder.glob("**/*.py"):
        spec = importlib.util.spec_from_file_location(file.name.rsplit(".", 1)[0], file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class:
                classes.append(obj)
    instances = []
    for class_ in classes:
        # noinspection PyBroadException
        try:
            instances.append(class_())
        except Exception:
            pass
    return instances


def load_inputs():
    return load_classes(Path("inputs"), InputBase)


def load_generators():
    return load_classes(Path("generators"), GeneratorBase)


def load_outputs():
    return load_classes(Path("outputs"), OutputBase)


def patch_image_hashable():
    from PIL.PngImagePlugin import PngImageFile

    def __hash__(self):
        import hashlib
        return int(hashlib.md5(self.tobytes()).hexdigest(), 16)
    PngImageFile.__hash__ = __hash__

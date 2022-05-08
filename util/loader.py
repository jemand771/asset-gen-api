import importlib.util
import inspect
from pathlib import Path
from util.types import GeneratorBase, InvalidInputError, OutputBase


registry = None


class Registry:

    def __init__(self):
        self.generators = self.load_classes(Path("generators"), GeneratorBase)
        self.outputs = self.load_classes(Path("outputs"), OutputBase)

    @staticmethod
    def load_classes(folder: Path, base_class):
        classes = []
        for file in folder.glob("**/*.py"):
            spec = importlib.util.spec_from_file_location("generators." + file.name.rsplit(".", 1)[0], file)
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
                print(f"failed to init {class_}")
        return instances

    def find_output(self, output_type, name_selector=None):
        for output_candidate in self.outputs:
            if output_candidate.name is None:
                continue
            if output_candidate.type != output_type:
                continue
            if not name_selector or output_candidate.name == name_selector:
                return output_candidate
        raise InvalidInputError(f"no suitable output found {output_type=} {name_selector=}")

    def find_output_by_class(self, class_):
        return self.find_output(class_.type, class_.name)

    def find_generator(self, name, output_type):
        for generator in self.generators:
            if generator.name == name and generator.type == output_type:
                return generator
        raise InvalidInputError(f"no suitable generator found: '{name=}'")

    def find_generator_by_class(self, class_):
        return self.find_generator(class_.name, class_.type)

def init_registry():
    global registry
    registry = Registry()


def patch_image_hashable():
    from PIL.PngImagePlugin import PngImageFile
    from PIL.Image import Image

    def __hash__(self):
        import hashlib
        return int(hashlib.md5(self.tobytes()).hexdigest(), 16)
    PngImageFile.__hash__ = __hash__
    Image.__hash__ = __hash__

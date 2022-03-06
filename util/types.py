from enum import Enum, auto


class MediaType(Enum):
    text = auto()
    image = auto()


class GeneratorBase:
    input_params: dict
    name: str = None
    output_type: MediaType

    def run(self, **kwargs):
        pass


class InputBase:
    name: str = None
    params: dict
    type: MediaType

    def get_value(self, **kwargs):
        pass


class OutputBase:
    name: str = None
    type: MediaType

    def make_response(self, *args, **kwargs):
        pass

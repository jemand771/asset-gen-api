from PIL import Image

from util.parse import parse_color
from util.types import GeneratorBase, MediaType


class SingleColorImage(GeneratorBase):
    input_params = {
        "color": MediaType.text,
        "dim": MediaType.integer
    }
    name = "color_square"
    type = MediaType.image

    def run(self, color, dim=400):
        color = parse_color(color)
        color_format = "RGB" if len(color) == 3 else "RGBA"
        # pycharm complains about "str instead of literal" here - it's technically correct, but eh ¯\_(ツ)_/¯
        # noinspection PyTypeChecker
        img = Image.new(color_format, (dim, dim), color)
        return img

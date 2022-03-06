from PIL import Image

from util.types import GeneratorBase, MediaType
from util.parse import parse_color


class SingleColorImage(GeneratorBase):
    input_params = {
        "color": MediaType.text
    }
    name = "color_square"
    output_type = MediaType.image

    def run(self, color):
        color = parse_color(color)
        color_format = "RGB" if len(color) == 3 else "RGBA"
        # pycharm complains about "str instead of literal" here - it's technically correct, but eh ¯\_(ツ)_/¯
        # noinspection PyTypeChecker
        img = Image.new(color_format, (400, 400), color)
        return img

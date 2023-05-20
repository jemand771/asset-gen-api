from PIL.Image import Image

from util.types import GeneratorBase


class TextEcho(GeneratorBase):
    type = "echo.text"

    def run(self, text: str) -> str:
        return text


class ImageEcho(GeneratorBase):
    type = "echo.image"

    def run(self, image: Image) -> Image:
        return image

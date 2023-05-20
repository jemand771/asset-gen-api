from PIL.Image import Image

from util.types import Box, GeneratorBase


class ForegroundPaste(GeneratorBase):
    type = "fgpaste"

    def run(self, canvas: Image, image: Image, box: Box) -> Image:
        image = image.resize(size=box.dim)
        canvas.paste(image, box.xyxy, image)
        return canvas


class BackgroundPaste(GeneratorBase):
    type = "bgpaste"

    def run(self, canvas: Image, image: Image, mask: Image, box: Box) -> Image:
        image = image.resize(size=box.dim)
        mask = mask.crop(box.xyxy).convert("L")
        canvas.paste(image, box.xyxy, mask)
        return canvas

from PIL import Image

from util.types import GeneratorBase, MediaType


class ForegroundPaste(GeneratorBase):
    input_params = {
        "canvas": MediaType.image,
        "image": MediaType.image,
        "box": MediaType.box,
    }
    name = "fgpaste"
    output_type = MediaType.image

    def run(self, canvas: Image.Image, image: Image.Image, box):
        image = image.resize(size=box.dim)
        canvas.paste(image, box.xyxy, image)
        return canvas


class BackgroundPaste(GeneratorBase):
    input_params = {
        "canvas": MediaType.image,
        "image": MediaType.image,
        "mask": MediaType.image,
        "box": MediaType.box,
    }
    name = "bgpaste"
    output_type = MediaType.image

    def run(self, canvas: Image.Image, image, mask, box):
        image = image.resize(size=box.dim)
        mask = mask.crop(box.xyxy).convert("L")
        canvas.paste(image, box.xyxy, mask)
        return canvas

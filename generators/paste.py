from PIL import Image

from util.types import GeneratorBase, MediaType


class ForegroundPaste(GeneratorBase):
    input_params = {
        "canvas": MediaType.image,
        "image": MediaType.image,
        "x1": MediaType.integer,
        "y1": MediaType.integer,
        "x2": MediaType.integer,
        "y2": MediaType.integer,
        # TODO refactor 4 coords into box type
    }
    name = "fgpaste"
    output_type = MediaType.image

    def run(self, canvas: Image.Image, image: Image.Image, x1, y1, x2, y2):
        target_box = (x1, y1, x2, y2)
        image = image.resize(size=(x2 - x1, y2 - y1))
        canvas.paste(image, target_box)
        return canvas


class BackgroundPaste(GeneratorBase):
    input_params = {
        "canvas": MediaType.image,
        "image": MediaType.image,
        "mask": MediaType.image,
        "x1": MediaType.integer,
        "y1": MediaType.integer,
        "x2": MediaType.integer,
        "y2": MediaType.integer,
    }
    name = "bgpaste"
    output_type = MediaType.image

    def run(self, canvas: Image.Image, image, mask, x1, y1, x2, y2):
        target_box = (x1, y1, x2, y2)
        image = image.resize(size=(x2 - x1, y2 - y1))
        mask = mask.crop(target_box).convert("L")
        canvas.paste(image, target_box, mask)
        return canvas

from PIL import Image

from util.types import GeneratorBase, MediaType


class StitchImages(GeneratorBase):
    input_params = {
        "image1": MediaType.image,
        "image2": MediaType.image,
        "vertical": MediaType.text,
    }
    name = "stitch"
    output_type = MediaType.image

    def run(self, image1, image2, vertical=False):
        # TODO scale
        # TODO proper boolean type
        x1, y1 = image1.size
        x2, y2 = image2.size
        dim = (max(x1, x2), y1 + y2) if vertical else (x1 + x2, max(y1, y2))
        img = Image.new("RGBA", dim)
        img.paste(image1)
        append_x, append_y = (0, y1) if vertical else (x1, 0)
        img.paste(image2, (append_x, append_y, append_x + x2, append_y + y2))
        return img

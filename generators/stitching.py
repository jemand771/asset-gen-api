from PIL import Image

from util.types import GeneratorBase


class StitchImages(GeneratorBase):
    type = "stitch"

    def run(self, image1: Image.Image, image2: Image.Image, vertical: bool = False) -> Image.Image:
        # TODO scale
        x1, y1 = image1.size
        x2, y2 = image2.size
        dim = (max(x1, x2), y1 + y2) if vertical else (x1 + x2, max(y1, y2))
        img = Image.new("RGBA", dim)
        img.paste(image1)
        append_x, append_y = (0, y1) if vertical else (x1, 0)
        img.paste(image2, (append_x, append_y, append_x + x2, append_y + y2))
        return img

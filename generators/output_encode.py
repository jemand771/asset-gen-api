import io

from PIL.Image import Image

from util.types import GeneratorBase


class PNGEncoder(GeneratorBase):
    type = "_img_to_png_buf"

    def run(self, image: Image) -> bytes:
        img_io = io.BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)
        return img_io.read()

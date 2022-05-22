import io

from util.types import GeneratorBase, MediaType


class PNGEncoder(GeneratorBase):
    type = MediaType.bytes
    # TODO make generators starting in _ unavailable externally
    # or mark them as private using a member flag
    name = "_img_to_png_buf"
    input_params = {
        "image": MediaType.image
    }

    def run(self, image):
        img_io = io.BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)
        return img_io.read()

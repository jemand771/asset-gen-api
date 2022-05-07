from util.types import Box, GeneratorBase, MediaType


class ZeroBoundBox(GeneratorBase):
    input_params = {
        "width": MediaType.integer,
        "height": MediaType.integer,
    }
    name = "box_wh"
    output_type = MediaType.box

    def run(self, width, height):
        return Box.from_xywh(0, 0, width, height)

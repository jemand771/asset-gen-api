from util.types import Box, GeneratorBase


class ZeroBoundBox(GeneratorBase):
    type = "box_wh"

    def run(self, width: int, height: int) -> Box:
        return Box.from_xywh(0, 0, width, height)

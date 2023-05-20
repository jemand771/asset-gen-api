from PIL import Image

from util.types import GeneratorBase


class RotateImage(GeneratorBase):
    type = "rotate"

    def run(self, image: Image.Image, angle: float, expand: bool = False) -> Image.Image:
        return image.rotate(angle, expand=expand)


class CropImageRatio(GeneratorBase):
    type = "rcrop"

    @staticmethod
    def _size_ratio(image):
        return image.size[0] / image.size[1]

    def run(self, image: Image.Image, x: int, y: int, pos: int = 50) -> Image.Image:
        source_ratio = self._size_ratio(image)
        target_ratio = x / y
        if source_ratio == target_ratio:
            return image
        if source_ratio < target_ratio:
            # image is too tall -> crop y
            y_size = image.size[0] // target_ratio
            y_move = (image.size[0] - y_size) * pos // 100
            return image.crop((0, y_move, image.size[0], y_size + y_move))
        if source_ratio > target_ratio:
            # image is too wide -> crop x
            x_size = image.size[1] * target_ratio
            x_move = (image.size[1] - x_size) * pos // 100
            return image.crop((x_move, 0, x_size + x_move, image.size[1]))

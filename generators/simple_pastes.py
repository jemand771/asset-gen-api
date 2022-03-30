import math

from generators.image_from_url import ImageFromServerAsset
from generators.paste import BackgroundPaste
from generators.transform import CropImageRatio, RotateImage
from util.types import GeneratorBase, MediaType


class GaybillGenerator(GeneratorBase):
    input_params = {
        "image": MediaType.image
    }
    name = "gaybill"
    output_type = MediaType.image

    def run(self, image):
        # TODO box class
        x1 = 575
        x2 = 855
        y1 = 45
        y2 = 260
        # TODO maybe turn the crop+rotate chain into one generator
        return BackgroundPaste().run(
            image=RotateImage().run(
                CropImageRatio().run(
                    image,
                    math.cos(15) * (x2 - x1),
                    math.cos(15) * (y2 - y1),
                    50
                ),
                15,
                True
            ),
            canvas=ImageFromServerAsset().run("gaybill.png"),
            mask=ImageFromServerAsset().run("gaybill_mask.png"),
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2
        )
    # TODO internal instance registry

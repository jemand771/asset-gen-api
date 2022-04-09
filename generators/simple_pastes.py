import math

from generators.image_from_url import ImageFromServerAsset
from generators.paste import BackgroundPaste
from generators.transform import CropImageRatio, RotateImage
from util.types import GeneratorChain, MappedParam, MediaType, Runner


class GaybillGenerator(GeneratorChain):
    input_params = {
        "image": MediaType.image
    }
    name = "gaybill"
    output_type = MediaType.image

    x1 = 575
    x2 = 855
    y1 = 45
    y2 = 260
    chain = Runner(
        BackgroundPaste,
        image=Runner(
            RotateImage,
            image=Runner(
                CropImageRatio,
                image=MappedParam(name="image"),
                x=math.cos(15) * (x2 - x1),
                y=math.cos(15) * (y2 - y1),
                pos=50
            ),
            angle=15,
            expand=True
        ),
        canvas=Runner(
            ImageFromServerAsset,
            name="gaybill.png"
        ),
        mask=Runner(
            ImageFromServerAsset,
            name="gaybill_mask.png"
        ),
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2
    )

    # TODO box class
    # TODO maybe turn the crop+rotate chain into one generator
    # TODO internal instance registry

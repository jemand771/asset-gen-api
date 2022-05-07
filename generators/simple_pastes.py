import math

from generators.image_from_url import ImageFromServerAsset
from generators.paste import BackgroundPaste
from generators.transform import CropImageRatio, RotateImage
from util.types import Box, GeneratorChain, MappedParam, MediaType, Runner


class GaybillGenerator(GeneratorChain):
    input_params = {
        "image": MediaType.image
    }
    name = "gaybill"
    output_type = MediaType.image

    box = Box(x1=575, x2=855, y1=45, y2=260)
    chain = Runner(
        BackgroundPaste,
        image=Runner(
            RotateImage,
            image=Runner(
                CropImageRatio,
                image=MappedParam(name="image"),
                x=math.cos(15) * box.width,
                y=math.cos(15) * box.height,
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
        box=box
    )

    # TODO maybe turn the crop+rotate chain into one generator

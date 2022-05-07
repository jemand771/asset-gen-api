from generators.image_from_url import ImageFromServerAsset
from generators.paste import ForegroundPaste
from generators.text import BetterText
from util.types import Box, GeneratorChain, MappedParam, MediaType, Runner
from util.util import preprocess_string


class NoBitchesGenerator(GeneratorChain):
    input_params = {
        "text": MediaType.text
    }
    name = "no_bitches"
    output_type = MediaType.image

    box = Box(x1=20, x2=519, y1=20, y2=120)
    chain = Runner(
        ForegroundPaste,
        canvas=Runner(
            ImageFromServerAsset,
            name="megamind_no_bitches.png"
        ),
        box=box,
        image=Runner(
            BetterText,
            box=box.whbox,
            font=preprocess_string("impact", MediaType.font),
            fill_color=(255, 255, 255),
            stroke_color=(0, 0, 0, 255),
            stroke_width=5,
            text=MappedParam(name="text")
        )
    )

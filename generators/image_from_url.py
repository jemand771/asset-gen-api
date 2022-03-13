from pathlib import Path

import requests
from PIL import Image

from util.types import GeneratorBase, MediaType


class ImageFromUrl(GeneratorBase):
    input_params = {
        "url": MediaType.text
    }
    name = "fromurl"
    output_type = MediaType.image

    def run(self, url):
        r = requests.get(url, stream=True)
        img = Image.open(r.raw)
        return img


class ImageFromServerAsset(GeneratorBase):
    # TODO host via own path
    input_params = {
        "name": MediaType.text
    }
    name = "fromasset"
    output_type = MediaType.image

    def run(self, name):
        path = Path("assets") / name
        if not path.is_file():
            raise ValueError()  # TODO asset not found
        return Image.open(path).convert("RGBA")

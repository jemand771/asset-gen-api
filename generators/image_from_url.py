from pathlib import Path

import requests
from PIL import Image

from util.types import GeneratorBase, InvalidInputError


class ImageFromUrl(GeneratorBase):
    type = "fromurl"

    def run(self, url: str) -> Image.Image:
        r = requests.get(url, stream=True)
        img = Image.open(r.raw)
        return img


class ImageFromServerAsset(GeneratorBase):
    # TODO host via own path
    type = "fromasset"

    def run(self, name: str) -> Image.Image:
        path = Path("assets") / name
        if not path.is_file():
            raise InvalidInputError("no such asset found")
        return Image.open(path).convert("RGBA")

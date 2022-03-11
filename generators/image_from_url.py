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

from util.types import InputBase, MediaType

import requests
from PIL import Image


class ImageInput(InputBase):
    type = MediaType.image


class UrlImageInput(ImageInput):
    name = "url"
    params = ("url", )

    def get_value(self, url):
        r = requests.get(url, stream=True)
        img = Image.open(r.raw)
        return img

import re

import numpy as np
import pilmoji
from PIL import Image, ImageFont
from pilmoji import Pilmoji

from util.types import GeneratorBase, InvalidInputError, MediaType


class RenderEmoji(GeneratorBase):
    input_params = {
        "emoji": MediaType.text,
        "size": MediaType.integer
    }
    name = "render_emoji"
    type = MediaType.image

    _regex = re.compile(f"^{pilmoji.EMOJI_REGEX.pattern}$")

    def run(self, emoji, size=400):
        if not self._regex.match(emoji):
            raise InvalidInputError("no single emoji was provided")
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        font = ImageFont.truetype("assets/fonts/calibri.ttf", size)
        with Pilmoji(img) as pimg:
            pimg.text((0, 0), emoji, (0, 0, 0, 255), font)
        return img


class UnwrapEmoji(GeneratorBase):
    input_params = {
        "image": MediaType.image
    }
    name = "unwrap_emoji"
    type = MediaType.image

    def run(self, image):
        data = np.array(image.convert("RGBA"))
        alpha = data.T[3]
        trans_pixels = alpha < 255
        full_pixels = alpha == 255
        colors, count = np.unique(data[full_pixels.T].reshape((-1, 4)), axis=0, return_counts=True)
        bg_color = colors[count.argmax()]
        data[trans_pixels.T] = bg_color
        return Image.fromarray(data)

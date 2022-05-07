from PIL import Image, ImageDraw, ImageFont

from util.types import GeneratorBase, GeneratorInternalError, InvalidInputError, MediaType


class SingleText(GeneratorBase):
    input_params = {
        "text": MediaType.text,
        "font_size": MediaType.integer,
        "max_height": MediaType.integer,
        "max_width": MediaType.integer,
    }
    name = "text_single"
    output_type = MediaType.image

    def get_max_font_size(self, text, font, max_width, max_height):
        # TODO use box class ?
        # TODO unclutter do-while loop
        if max_width is None and max_height is None:
            raise InvalidInputError("either max_width or max_height (or both) are needed")
        font_size = 1
        text_size = self.estimate_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
                (max_height is not None and text_size[1] > max_height):
            raise GeneratorInternalError("can't fit text")
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
                    (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.estimate_text_size(font, font_size, text)

    # TODO get the font data from somewhere
    # TODO make a better version of this with multiline support
    @staticmethod
    def estimate_text_size(font_data, font_size, text):
        font = ImageFont.truetype(font_data, font_size)
        return font.getsize(text)

    def run(self, text, max_height=None, max_width=None, font_size=None):
        font = "C:/Windows/Fonts/calibri.ttf"  # TODO get this from somewhere
        if font_size is None:
            font_size = self.get_max_font_size(text, font, max_height, max_width)
        text_size = self.estimate_text_size(font, font_size, text)
        img = Image.new("RGBA", text_size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=ImageFont.truetype(font, font_size), fill=(255, 0, 0))
        return img

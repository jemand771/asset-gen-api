import textwrap

from PIL import Image, ImageDraw, ImageFont

from util.types import Box, GeneratorBase, GeneratorInternalError, InvalidInputError, MediaType


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
        return font.getsize_multiline(text)

    def run(self, text, max_height=None, max_width=None, font_size=None):
        font = "C:/Windows/Fonts/calibri.ttf"  # TODO get this from somewhere
        if font_size is None:
            font_size = self.get_max_font_size(text, font, max_height, max_width)
        text_size = self.estimate_text_size(font, font_size, text)
        img = Image.new("RGBA", text_size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=ImageFont.truetype(font, font_size), fill=(255, 0, 0))
        return img


class BetterText(SingleText):
    input_params = {
        "text": MediaType.text,
        "font_size": MediaType.integer,
        # this is more of a "wanted" / max size than an exact prediction
        "box": MediaType.box,
        "fill_color": MediaType.color,
        "font": MediaType.font
    }
    name = "text_smart"
    output_type = MediaType.image

    @staticmethod
    def wrap_text(text, ratio, estimator):
        # this reminds me fo the bug that would bootloop iphones trying to shorten RTL text, lol
        # calling it now, this will break.
        # https://www.youtube.com/watch?v=hJLMSllzoLA
        best_text = text
        prev_ratio = None
        for max_line_len in reversed(range(1, len(text) + 1)):
            wrapped_text = "\n".join(textwrap.wrap(text, width=max_line_len))
            new_size = estimator(wrapped_text)
            new_ratio = new_size[0] / new_size[1]
            if prev_ratio is not None and abs(prev_ratio - ratio) < abs(new_ratio - ratio):
                return best_text
            prev_ratio = new_ratio
            best_text = wrapped_text
        raise GeneratorInternalError("could not wrap text")

    # noinspection PyMethodOverriding
    def run(self, text, box, font, fill_color=(0, 0, 0)):
        text = self.wrap_text(text, box.ratio, lambda t: self.estimate_text_size(font, 72, t))
        font_size = self.get_max_font_size(text, font, *box.dim)
        text_size = self.estimate_text_size(font, font_size, text)
        img = Image.new("RGBA", box.dim, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        target_x = box.width / 2 - text_size[0] / 2
        target_y = box.height / 2 - text_size[1] / 2
        draw.text(
            (target_x, target_y),
            text,
            font=ImageFont.truetype(font, font_size),
            fill=fill_color,
            align="center"
        )
        return img

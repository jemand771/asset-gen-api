import textwrap

from PIL import Image, ImageDraw, ImageFont

from util.types import Box, GeneratorBase, GeneratorInternalError, InvalidInputError


class SingleText(GeneratorBase):
    type = "text_single"

    # TODO abandoned class (for now)

    def get_max_font_size(self, font, max_width, max_height, **kwargs):
        # TODO use box class ?
        # TODO unclutter do-while loop
        if max_width is None and max_height is None:
            raise InvalidInputError("either max_width or max_height (or both) are needed")
        font_size = 1
        text_size = self.estimate_text_size(font, font_size, **kwargs)
        if (max_width is not None and text_size[0] > max_width) or \
            (max_height is not None and text_size[1] > max_height):
            raise GeneratorInternalError("can't fit text")
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
                (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.estimate_text_size(font, font_size, **kwargs)

    # TODO get the font data from somewhere
    # TODO make a better version of this with multiline support
    @staticmethod
    def estimate_text_size(font_path, font_size, **kwargs):
        font = ImageFont.truetype(font_path, font_size)
        img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(img)
        # https://github.com/python-pillow/Pillow/issues/5816
        box = Box.from_xyxy(*draw.multiline_textbbox((0, 0), font=font, **kwargs))
        # return p2 instead of dim to account for "extra" space on the left that...
        # honestly, I don't know why this works
        return box.p2

    def run(self, text: str, max_height: int = None, max_width: int = None, font_size: int = None) -> Image.Image:
        font = "C:/Windows/Fonts/calibri.ttf"  # TODO get this from somewhere
        if font_size is None:
            font_size = self.get_max_font_size(font, max_height, max_width, text=text)
        text_size = self.estimate_text_size(font, font_size, text=text)
        img = Image.new("RGBA", text_size, (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, font=ImageFont.truetype(font, font_size), fill=(255, 0, 0))
        return img


class BetterText(SingleText):
    type = "text_smart"

    @staticmethod
    def wrap_text(text, ratio, estimator):
        # this reminds me fo the bug that would bootloop iphones trying to shorten RTL text, lol
        # calling it now, this will break.
        # https://www.youtube.com/watch?v=hJLMSllzoLA
        if len(text) < 2:
            return text
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

    # TODO font data type
    # TODO color data type
    # noinspection PyMethodOverriding
    def run(
        self,
        text: str,
        box: Box,
        font: str,
        fill_color: tuple = (0, 0, 0),
        stroke_color: tuple = (0, 0, 0),
        stroke_width: int = 1
    ):
        img = Image.new("RGBA", box.dim, (0, 0, 0, 0))
        if not text:
            return img
        static_text_kwargs = dict(
            stroke_width=stroke_width,
            align="center"
        )
        text = self.wrap_text(
            text,
            box.ratio,
            lambda t: self.estimate_text_size(
                font_path=font,
                font_size=72,
                **static_text_kwargs,
                text=t
            )
        )
        font_size = self.get_max_font_size(font, *box.dim, text=text, **static_text_kwargs)
        text_size = self.estimate_text_size(font, font_size, text=text, **static_text_kwargs)
        draw = ImageDraw.Draw(img)
        target_x = box.width / 2 - text_size[0] / 2
        target_y = box.height / 2 - text_size[1] / 2
        draw.text(
            (target_x, target_y),
            text,
            font=ImageFont.truetype(font, font_size),
            fill=fill_color,
            stroke_fill=stroke_color,
            stroke_width=stroke_width,
            align="center"
        )
        return img

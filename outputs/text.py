from util.types import MediaType, OutputBase


class TextOutputBase(OutputBase):
    type = MediaType.text


class BodyOutput(TextOutputBase):
    name = "body"

    def run(self, text):
        return text

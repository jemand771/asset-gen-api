from util.types import InputBase, MediaType


class TextInput(InputBase):
    type = MediaType.text


class RawTextInput(TextInput):
    name = "raw"
    params = ("text",)

    def run(self, text):
        return text

from util.types import InputBase, MediaType


class TextInput(InputBase):
    type = MediaType.text


class RawTextInput(TextInput):
    name = "raw"
    params = ("text",)

    def get_value(self, text):
        return text

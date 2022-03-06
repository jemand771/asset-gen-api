from util.types import MediaType, OutputBase


# TODO TextOutputBase
class BodyOutput(OutputBase):
    name = "body"
    type = MediaType.text

    def make_response(self, text):
        return text

from util.types import MediaType, OutputBase


# TODO TextOutputBase
class BodyOutput(OutputBase):
    name = "body"
    type = MediaType.text

    def run(self, text):
        return text

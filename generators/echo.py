from util.types import GeneratorBase, MediaType


class TextEcho(GeneratorBase):

    input_params = {
        "text": MediaType.text
    }
    output_type = MediaType.text
    name = "echo"

    def run(self, text):
        return text


class ImageEcho(GeneratorBase):
    input_params = {
        "image": MediaType.image
    }
    output_type = MediaType.image
    name = "echo"

    def run(self, image):
        return image

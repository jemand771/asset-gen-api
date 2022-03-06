from util.types import GeneratorBase, MediaType


class Echo(GeneratorBase):

    input_params = {
        "text": MediaType.text
    }
    output_type = MediaType.text
    name = "echo"

    def run(self, text):
        return text

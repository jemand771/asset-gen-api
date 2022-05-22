import copy
import io

import flask

from generators.output_encode import PNGEncoder
from util import loader
from util.types import GeneratorInternalError, MediaType, OutputBase


class ImageOutputBase(OutputBase):
    type = MediaType.image


class BodyImageOutput(ImageOutputBase):
    name = "body"

    def run(self, img):
        if img is None:
            raise GeneratorInternalError("the generator returned None")
        img_bytes = copy.deepcopy(loader.registry.find_generator_by_class(PNGEncoder)).run(image=img)
        return flask.send_file(io.BytesIO(img_bytes), mimetype='image/png')

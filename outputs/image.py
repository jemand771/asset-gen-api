import io

import flask

from util.types import GeneratorInternalError, MediaType, OutputBase


class ImageOutputBase(OutputBase):
    type = MediaType.image


class BodyImageOutput(ImageOutputBase):
    name = "body"

    def run(self, img):
        if img is None:
            raise GeneratorInternalError("the generator returned None")
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return flask.send_file(img_io, mimetype='image/png')

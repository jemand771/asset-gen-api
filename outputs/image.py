import io

import flask

from util.types import MediaType, OutputBase


# TODO ImageOutputBase
class BodyImageOutput(OutputBase):
    name = "body"
    type = MediaType.image

    def make_response(self, img):
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return flask.send_file(img_io, mimetype='image/png')

import io
from typing import Any

import flask
from PIL.Image import Image


# TODO I don't really want this, but it's better than adding a png encoder to every graph for now.
# TODO think about other implicit casts (along the chain but mostly for inputs)
def implicit_encode(val: Any):
    if isinstance(val, Image):
        img_io = io.BytesIO()
        val.save(img_io, "PNG")
        img_io.seek(0)
        return flask.send_file(img_io, mimetype='image/png')
    return val

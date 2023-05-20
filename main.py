from typing import Any

from flask import Flask, abort, request

from util import loader, metrics
from util.encode import implicit_encode
from util.executor import Executor

loader.patch_image_hashable()
REGISTRY = loader.registry
metrics.init()

app = Flask(__name__)

metrics.route(app)


@app.get("/favicon.ico")
def favicon():
    abort(404)


@app.get("/preset/<preset_name>", strict_slashes=False)
def preset_handler_empty(preset_name):
    return preset_handler(preset_name, "")


@app.get("/preset/<preset_name>/<path:input_str>")
def preset_handler(preset_name, input_str):
    try:
        preset = REGISTRY.presets[preset_name]
    except KeyError:
        return abort(404)
    inputs: dict[str | None, Any] = {
        **request.args,
        None: input_str
    }
    return implicit_encode(
        Executor(REGISTRY, preset, inputs).execute()
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

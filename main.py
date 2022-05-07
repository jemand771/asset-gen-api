from flask import Flask, abort, request

from util import loader
from util.constants import PARAM_DELIMITER_GENERATOR_ARG, PARAM_DELIMITER_GENERATOR_GROUPS
from util.types import GeneratorBase, MediaType, OutputBase
from util.util import preprocess_string

loader.patch_image_hashable()
loader.init_registry()
REGISTRY = loader.registry

app = Flask(__name__)


@app.get("/<media_type>")
def handle_query(media_type):
    # TODO handle type error
    try:
        output_type = MediaType[media_type]
    except KeyError:
        # return because PyCharm doesn't see/understand the exception
        return abort(404, "unsupported media type")
    params = dict(request.args)
    # select a suitable output formatter
    output_handler = REGISTRY.find_output(output_type, name_selector=params.get("output"))
    # we got output_handler, now try to execute a generator
    try:
        params.pop("output")
    except KeyError:
        pass
    output = find_execute_generator(params, output_type)
    return output_handler.run(output)


def find_execute_generator(params: dict, output_type):
    arg_dict = {}
    grouped_args = group_input_params_once(params)
    generator_name, arg_names = get_generator_name_and_args(grouped_args)
    generator = REGISTRY.find_generator(generator_name, output_type)
    for key in arg_names:
        param_key = f"{generator_name}{PARAM_DELIMITER_GENERATOR_ARG}{key}"
        value = grouped_args[param_key]
        if isinstance(value, dict):
            # TODO no, wrong  # what did I mean by this
            arg_dict[key] = find_execute_generator(value, generator.input_params[key])
        else:
            arg_dict[key] = preprocess_string(value, generator.input_params[key])
    # arg_dict is fully resolved into non-nested key-value pairs
    # TODO handle TypeError for missing args
    return generator.run(**arg_dict)


def group_input_params_once(params):
    grouped = {}
    for key, value in params.items():
        try:
            new_key, right_side = key.split(PARAM_DELIMITER_GENERATOR_GROUPS, 1)
            grouped.setdefault(new_key, {})
            grouped[new_key][right_side] = value
        except ValueError:
            grouped[key] = value
    return grouped


def get_generator_name_and_args(grouped_args):
    # TODO error when no - in name
    generator_candidates, arg_names = zip(
        *[
            full_name.split(PARAM_DELIMITER_GENERATOR_ARG, 1)
            for full_name in grouped_args
        ]
    )
    if len(list(set(generator_candidates))) != 1:
        raise ValueError()  # TODO too many args
    return generator_candidates[0], arg_names


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

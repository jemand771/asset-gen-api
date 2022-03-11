from flask import Flask, abort, request

from util import loader
from util.types import GeneratorBase, OutputBase, MediaType
from util.constants import PARAM_DELIMITER_GENERATOR_ARG, PARAM_DELIMITER_GENERATOR_GROUPS

loader.patch_image_hashable()

GENERATORS = loader.load_generators()
OUTPUTS = loader.load_outputs()

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
    wanted_output = params.get("output")
    for output_candidate in OUTPUTS:
        if output_candidate.name is None:
            continue
        if output_candidate.type != output_type:
            continue
        if not wanted_output or output_candidate.name == wanted_output:
            output_handler: OutputBase = output_candidate
            break
    else:
        return "no output matched"  # TODO proper errors
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
    generator = find_generator(generator_name, output_type)
    if list(sorted(arg_names)) != list(sorted(generator.input_params)):
        raise ValueError()  # TODO error missing param
    for key in arg_names:
        param_key = f"{generator_name}{PARAM_DELIMITER_GENERATOR_ARG}{key}"
        value = grouped_args[param_key]
        if isinstance(value, dict):
            # TODO no, wrong
            arg_dict[key] = find_execute_generator(value, generator.input_params[key])
        else:
            arg_dict[key] = value
    # arg_dict is fully resolved into non-nested key-value pairs
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
    generator_candidates, arg_names = zip(*[
        full_name.split(PARAM_DELIMITER_GENERATOR_ARG, 1)
        for full_name in grouped_args
    ])
    if len(list(set(generator_candidates))) != 1:
        raise ValueError()  # TODO too many args
    return generator_candidates[0], arg_names


def find_generator(name, output_type):
    for generator in GENERATORS:
        generator: GeneratorBase
        if generator.name == name and generator.output_type == output_type:
            return generator
    raise ValueError()  # TODO error generator not found


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


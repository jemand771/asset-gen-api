from flask import Flask, request

from util import loader
from util.types import GeneratorBase, InputBase, OutputBase

INPUTS = loader.load_inputs()
GENERATORS = loader.load_generators()
OUTPUTS = loader.load_outputs()

app = Flask(__name__)


def make_handler(generator: GeneratorBase):
    def handle():
        params = dict(request.args)
        # select a suitable output formatter
        wanted_output = params.get("output")
        for output_candidate in OUTPUTS:
            if output_candidate.name is None:
                continue
            if output_candidate.type != generator.output_type:
                continue
            if not wanted_output or output_candidate.name == wanted_output:
                output_handler: OutputBase = output_candidate
                break
        else:
            return "no output matched"  # TODO proper errors
        # TODO don't run input grabber yet? - validation vs. efficiency
        # collect input parameters
        collected_generator_inputs = {}
        for gen_param, gen_param_type in generator.input_params.items():
            for input_handler in INPUTS:
                input_handler: InputBase
                if input_handler.name is None:
                    continue
                if input_handler.type != gen_param_type:
                    continue
                if not all(f"{gen_param}-{p}" in params for p in input_handler.params):
                    continue
                collected_generator_inputs[gen_param] = input_handler.run(
                    **{
                        p_name: params.get(f"{gen_param}-{p_name}")
                        for p_name in input_handler.params
                    }
                )
                break
            else:
                return "no"  # TODO proper errors
        # execute generator
        generator_output = generator.run(**collected_generator_inputs)
        return output_handler.run(generator_output)

    handle.__name__ = f"handle_{generator.output_type.name}_{generator.name}"
    return handle


for generator_ in GENERATORS:
    app.get(f"/{generator_.output_type.name}/{generator_.name}")(make_handler(generator_))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

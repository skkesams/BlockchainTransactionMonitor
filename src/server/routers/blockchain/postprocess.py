import json
from core.utils import log_exception


def get_inputs(inputs):
    inp_keys = ["prev_hash", "output_value", "addresses"]
    inp_lst = []
    try:
        inputs = json.loads(inputs)
        for inp in inputs:
            inp_data = {}
            for k in inp_keys:
                inp_data[k] = inp[k]
            inp_lst.append(inp_data)
    except Exception as e:
        log_exception(e, "error while processing Inputs")
    return inp_lst


def get_outputs(outputs):
    out_keys = ["value", "addresses"]
    out_lst = []
    try:
        outputs = json.loads(outputs)
        for outp in outputs:
            out_data = {}
            for k in out_keys:
                out_data[k] = outp[k]
            out_lst.append(out_data)
    except Exception as e:
        log_exception(e, "error while processing outputs")
    return out_lst


async def postprocess(data):
    req_keys = ["hash", "total", "fees"]
    output = []
    try:
        for d in data:
            record = {}
            for k in req_keys:
                record[k] = d.get(k, None)
            inp = d.get("inputs", [])
            record["inputs"] = get_inputs(inp)
            out = d.get("outputs", [])
            record["outputs"] = get_outputs(out)

            output.append(record)
    except Exception as e:
        log_exception(e, "error while postprocessing")
    return output

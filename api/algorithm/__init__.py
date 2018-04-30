import json as js
import os

def gen_params():
    params = {}
    path = os.path.dirname(__file__)
    for root, dirs, files in os.walk(path):
        for name in files:
            if ".json" not in name[-5:]:
                continue
            with open(os.path.join(root, name)) as f:
                args = f.read()
                args = js.loads(args)
                args = {args["name"] : args}
                params.update(args)
    return params


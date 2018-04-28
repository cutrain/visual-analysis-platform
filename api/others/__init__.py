import json as js
import os
files = ['predict', 'sql-execute']

def gen_params():
    params = {}
    path = os.path.dirname(__file__)
    for name in files:
        with open(os.path.join(path, (name + '.json'))) as f:
            args = f.read()
            args = js.loads(args)
            args = {name : args}
            params.update(args)
    return params


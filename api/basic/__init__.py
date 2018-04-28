import json as js
import os
files = ['data-instream', 'data-outstream', 'model-instream', 'model-outstream', 'sql-instream', 'sql-outstream']

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


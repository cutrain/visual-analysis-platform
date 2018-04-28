import json as js

import algorithm
import basic
import data_process
import others

if __name__ == "__main__":
    params = {}
    params.update(algorithm.gen_params())
    params.update(basic.gen_params())
    params.update(data_process.gen_params())
    params.update(others.gen_params())
    with open('params.json', 'w') as f:
        data = js.dumps(params, indent=2, separators=(',',':'), ensure_ascii=False)
        f.write(data)


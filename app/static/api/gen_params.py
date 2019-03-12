import os
import json as js

import algorithm
import basic
import data_process
import others

if __name__ == "__main__":
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)

    params = {}
    params.update(algorithm.gen_params())
    params.update(basic.gen_params())
    params.update(data_process.gen_params())
    params.update(others.gen_params())

    inout_str = ['in0out1', 'in1out0' ,'in1out1', 'in1out2', 'in2out1', 'in2out2']
    for i in inout_str:
        command = i + '=[]'
        print(command)
        exec(command)

    # inout
    for name, value in params.items():
        inout = value.pop("inout")
        command = inout + '.append("' + name + '")'
        print(command)
        exec(command)
    inout_print = ""
    for i in inout_str:
        inout_print += i + '=['
        for j in eval(i):
            inout_print += '"' + j + '",'
        inout_print += ']\n'
    print(inout_print)
    with open('inout.js', 'w') as f:
        f.write(inout_print)
    with open('inout.py', 'w') as f:
        f.write(inout_print)

    # trans params
    for key in params:
        params[key] = params[key]["attr"]

    data = js.dumps(params, indent=2, separators=(',',':'), ensure_ascii=False)
    with open('params.json', 'w') as f:
        f.write(data)
    with open('params.js', 'w') as f:
        f.write('details = ')
        f.write(data)

    # html nodes display
    type_list = ['algorithm', 'basic', 'data_process', 'others']
    html_print = "type_id = {\n"
    for t in type_list:
        command = t + '.gen_params()'
        print(command)
        param = eval(command)
        html_print += '\t"' + t + '": {\n'
        for name, value in param.items():
            html_print += '\t\t"' + name + '":"' + value["display"] + '",\n'
        html_print += '\t},\n'
    html_print += '}'
    print(html_print)
    with open("nodes.js", "w") as f:
        f.write(html_print)


from config import component_dir
from . import component
from .. import db
from tool import msgwrap
from flask import render_template, request

import os
import json

@component.route('/list', methods=['POST'])
@msgwrap
def compo_list():
    global component_dir
    ret = {
        "structure":{},
    }
    with open(os.path.join(component_dir, 'structure.json'), 'rb') as f:
        structure = json.load(f)
    ret['structure'].update(structure)
    return ret

@component.route('/param', methods=['POST'])
@msgwrap
def compo_params():
    global component_dir
    fields = ['name', 'display', 'in_port', 'out_port', 'params']
    ret = {
        'component':[],
    }
    for root, dirs, files in os.walk(component_dir):
        for file in files:
            if file is not 'structure.json' and file[-5:] == '.json':
                with open(os.path.join(root, file), 'rb') as f:
                    data = json.load(f)
                if all([field in data for field in fields]):
                    ret['component'].append(data)
    return ret

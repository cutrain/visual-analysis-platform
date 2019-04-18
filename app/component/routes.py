from config import COMPONENT_DIR
from . import component
from .. import db
from tool import msgwrap
from flask import render_template, request

import os
import json

@component.route('/list', methods=['POST'])
@msgwrap
def compo_list():
    global COMPONENT_DIR
    ret = {
        "structure":{},
    }
    with open(os.path.join(COMPONENT_DIR, 'structure.json'), 'rb') as f:
        structure = json.load(f)
    ret['structure'].update(structure)
    return ret

@component.route('/param', methods=['POST'])
@msgwrap
def compo_params():
    global COMPONENT_DIR
    fields = ['name', 'display', 'in_port', 'out_port', 'params']
    ret = {
        'component':[],
    }
    for root, dirs, files in os.walk(COMPONENT_DIR):
        for file in files:
            if file is not 'structure.json' and file[-5:] == '.json':
                with open(os.path.join(root, file), 'rb') as f:
                    data = json.load(f)
                if all([field in data for field in fields]):
                    ret['component'].append(data)
    return ret

def check_format(detail):
    keys = ['name', 'display', 'params', 'in_port', 'out_port']
    # check detail format
    if not all(map(lambda x:x in detail, keys)):
        return {
            'succeed':1,
            'message': "miss key" + str(detail.keys()) + '/' + str(keys),
        }
    if len(detail['name']) == 0:
        return {
            'succeed':1,
            'message': 'name should not be empty',
        }
    if len(detail['display']) == 0:
        return {
            'succeed':1,
            'message': 'display should not be empty',
        }
    return None

def check_compo_exist(name):
    global COMPONENT_DIR
    if os.path.exists(os.path.join(COMPONENT_DIR, 'function', name+'.json')):
        return {
            'succeed': 1,
            'message': "rename component name already exist",
        }
    return None

@component.route('/modify', methods=['POST'])
@msgwrap
def compo_modify():
    global COMPONENT_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    component_id = req.pop('component_id')
    detail = req.pop('detail')

    # check component name
    ret = check_format(detail)
    if ret is not None:
        return ret

    if component_id != detail['name']:
        ret = check_compo_exist(detail['name'])
        if ret is not None:
            return ret

    with open(os.path.join(COMPONENT_DIR, 'structure.json'), 'rb') as f:
        structure = json.load(f)
    def walk(obj, id, new_id, display):
        if type(obj) != dict:
            return False
        ret = False
        if id in obj:
            if id != new_id:
                obj.pop(id)
                obj.update({new_id:display})
            else:
                obj[id] = display
            return True
        for key, val in obj.items():
            ret = ret and walk(val, id, new_id, display)
        return ret

    ret = walk(structure, component_id, detail['name'], detail['display'])
    if not ret:
        return {
            'succeed':1,
            'message': component_id + ' not found',
        }
    with open(os.path.join(COMPONENT_DIR, 'structure.json'), 'w') as f:
        f.write(json.dumps(structure, ensure_ascii=False, indent=2))

    with open(os.path.join(COMPONENT_DIR, 'function', detail['name']+'.json'), 'w') as f:
        f.write(json.dumps(detail, ensure_ascii=False, indent=2))
    if detail['name'] != component_id:
        old_file = os.path.join(COMPONENT_DIR, 'function', component_id+'.json')
        if os.path.exists(old_file):
            os.remove(old_file)



@component.route('/create', methods=['POST'])
@msgwrap
def compo_create():
    global COMPONENT_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    detail = req.pop('detail')
    class_ = req.pop('class')
    print('detail', detail)
    print('calss', class_)

    ret = check_format(detail)
    if ret is not None:
        return ret

    ret = check_compo_exist(detail['name'])
    if ret is not None:
        return ret

    # change structure
    with open(os.path.join(COMPONENT_DIR, 'structure.json'), 'rb') as f:
        structure = json.load(f)
    posi = class_.split('-')[1:]
    now = structure
    for i in posi:
        now = now[i]
    now[detail['name']] = detail['display']
    with open(os.path.join(COMPONENT_DIR, 'structure.json'), 'w') as f:
        f.write(json.dumps(structure, ensure_ascii=False, indent=2))

    # save component
    with open(os.path.join(COMPONENT_DIR, 'function', detail['name']+'.json'), 'w') as f:
        f.write(json.dumps(detail, ensure_ascii=False, indent=2))


@component.route('/getcode', methods=['POST'])
@msgwrap
def compo_getcode():
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    component_id = req.pop('component_id')
    print('component id', component_id)
    # TODO : get code

@component.route('/modifycode', methods=['POST'])
@msgwrap
def compo_modifycode():
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    component_id = req.pop('component_id')
    code = req.pop('code')
    print('component id', component_id)
    print('code', code)
    # TODO : modify code


from . import data
from .. import db
from ..tool import msgwrap
from flask import render_template, request

@data.route('/upload', methods=['POST'])
@msgwrap
def upload():
    # TODO
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    get_f = request['file']
    path = req.pop('dataset')
    with open(os.path.join('data', path), 'wb') as f:
        f.write(get_f)

    return {
        "size":213,
    }

@data.route('/view', methods=['POST'])
@msgwrap
def view():
    # TODO
    pass

@data.route('/get', methods=['POST'])
@msgwrap
def get():
    # TODO
    pass

@data.route('/move', methods=['POST'])
@msgwrap
def move():
    # TODO
    pass

@data.route('/delete', methods=['POST'])
@msgwrap
def delete():
    # TODO
    pass


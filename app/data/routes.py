from . import data
from .. import db
from flask import render_template

@data.route('/')
def index():
    return render_template('index.html')

from . import main
from .. import db
from ..models import Hello
from flask import render_template, request

from .analysis import analysis

import os
import redis
import json as js
import pandas as pd

r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)

@main.route('/')
def index():
    return render_template("main/index.html")

@main.route('/run', methods=['POST'])
def run():
    a = request.get_data().decode('utf-8')
    a = js.loads(a)
    print(a)
    analysis(a)
    tmp = {"status":0}
    return js.dumps(tmp)

@main.route('/progress', methods=['POST'])
def progress():
    progress = r.hgetall('status')
    print(progress)
    status = r.get('global')
    print(status)
    if status != '0':
        status = '1'

    tmp = {
        "status":status,
        "progress":progress
    }
    return js.dumps(tmp)



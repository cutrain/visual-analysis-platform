import time
import random
import string
import filetype
import json as js
from functools import wraps

def msgwrap(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        ret = {
            'succeed':0,
            'message':'succeed',
        }
        try:
            result = func(*args, **kwargs)
            if type(result) is dict:
                ret.update(result)
        except Exception as e:
            print('error', e, flush=True)
            ret = {
                'succeed':1,
                'message':str(e),
            }
        print(ret, flush=True)
        return js.dumps(ret).encode('utf-8')
    return wrap

def gen_random_string(length=8, *, number=True, abc=True, upper_case=False, lower_case=False):
    charset = ''
    if number:
        charset += string.digits
    if abc:
        if upper_case==lower_case:
            charset += string.ascii_letters
        elif upper_case:
            charset += string.ascii_uppercase
        elif lower_case:
            charset += string.ascii_lowercase
    return ''.join(random.choice(charset) for _ in range(length))

def get_type(filepath=None, data=None):
    if filepath is not None:
        ans = filetype.guess(filepath)
        if ans is None:
            return 'DataFrame'
        if ans.find('image') != -1:
            return "Image"
        if ans.find('video') != -1:
            return 'Video'
        if ans.find('audio') != -1:
            return 'Audio'
        # TODO : more type
    return "DataFrame"

def safepath(path):
    path = path.replace('..', '')
    path = path.lstrip('/')
    return path


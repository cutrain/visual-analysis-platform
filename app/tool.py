import time
import random
import string
import json as js
def msgwrap(func):
    def wrap(*args, **kwargs):
        ret = {
            'succeed':1,
            'message':'succeed',
        }
        try:
            result = func(*args, **kwargs)
            if result is not None:
                ret.update(result)
        except Exception as e:
            ret = {
                'succeed':0,
                'message':str(e),
            }
        return js.dumps(ret).encode('utf-8')
    return wrap

def gen_random_string(length=8, *, number=True, abc=True, upper_case=False, lower_case=False):
    charset = 0
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




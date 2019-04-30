import os
from config import DATA_DIR, PROJECT_DIR, CACHE_DIR
from app import create_app
from flask_script import Manager

app = create_app('default')
manager = Manager(app)

def init():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)
    if not os.path.exists(PROJECT_DIR):
        os.mkdir(PROJECT_DIR)
    if not os.path.exists(CACHE_DIR):
        os.mkdir(CACHE_DIR)

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)

    init()

    manager.run()

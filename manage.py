import os
from config import data_dir, model_dir, project_dir, cache_dir
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import pymysql
pymysql.install_as_MySQLdb()

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

def init():
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)

    init()

    manager.run()

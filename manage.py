import os
from app import create_app, db
from app.models import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import pymysql
pymysql.install_as_MySQLdb()

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

def init():
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("model"):
        os.mkdir("model")

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)

    init()

    manager.run()

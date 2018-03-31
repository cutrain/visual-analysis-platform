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

if __name__ == '__main__':
    manager.run()

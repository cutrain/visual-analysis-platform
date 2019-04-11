import logging
from logging.handlers import RotatingFileHandler

redis_host = 'localhost'
redis_port = 6379
redis_db = 0


account = 'root'
passwd = '123'
database = 'test'

data_dir = 'data'
model_dir = 'model'
component_dir = 'component'
project_dir = 'project'
cache_dir = 'cache'


class Config:
    SECRET_KEY = "" # TODO: set the key
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        handler = RotatingFileHandler('back.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + account + ':' + passwd + '@localhost/' + database
    DEBUG = True


config = {
    'default': DevelopmentConfig
}


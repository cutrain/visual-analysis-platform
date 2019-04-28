import logging
from logging.handlers import RotatingFileHandler

DEBUG = True
DEVELOP = True

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

DATA_DIR= 'data'
COMPONENT_DIR= 'component'
PROJECT_DIR= 'project'
CACHE_DIR = 'cache'

STATIC_PATH = ''


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
    global ACCOUNT, PASSWD, DATABASE
    DEBUG = True


config = {
    'default': DevelopmentConfig
}


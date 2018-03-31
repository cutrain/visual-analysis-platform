import logging
from logging.handlers import RotatingFileHandler

account = 'root'
passwd = '123'
database = 'test'


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


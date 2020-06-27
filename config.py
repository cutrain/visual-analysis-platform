import sys
import logging

DEBUG = True
DEVELOP = True

logger = logging.getLogger(__name__)
level = logging.DEBUG if DEBUG else logging.INFO
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(level=level)

# StreamHandler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level=level)
stream_handler.setFormatter(formatter)
if DEVELOP:
    logger.addHandler(stream_handler)

# FileHandler
file_handler = logging.FileHandler('output.log')
file_handler.setLevel(level=level)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)




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
        return


class DevelopmentConfig(Config):
    global ACCOUNT, PASSWD, DATABASE
    DEBUG = False


config = {
    'default': DevelopmentConfig
}


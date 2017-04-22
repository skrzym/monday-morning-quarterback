class BaseConfig(object):
    DEBUG = False
    TESTING  = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

from flask_pymongo import PyMongo
mongo = PyMongo()

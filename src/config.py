import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'verysecret'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///community.db'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'undefined')
    SECRET_KEY = os.environ.get('SECRET_KEY', Config.SECRET_KEY)
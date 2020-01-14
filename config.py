import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nopassw0rd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE = os.path.join(basedir, 'database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE = os.path.join(basedir, 'database.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE = os.path.join(basedir, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + SQLALCHEMY_DATABASE

import os
import logging
import socket

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    ZTGG_DOMAIN = socket.gethostname()

    MONGO_PORT = 55001
    MONGO_DB_NAME = "ztgg_demo_db"
    MONGO_URL = 'mongodb://{}:{}/'.format(ZTGG_DOMAIN, MONGO_PORT)

    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG

    ABC = "abc"
    APPLICATION_ROOT = '/ztgg-backend-api/v1/'

    DEFAULT_CREATOR = "App_Admin"

    # JWT Part
    # JWT_AUTH_HEADER_PREFIX = 'CST_TOKEN'
    # JWT_AUTH_URL_RULE = '/cst-ui-api/v1/cst_auth'
    # JWT_EXPIRATION_DELTA = timedelta(days=365*5)
    # JWT_AUTH_PASSWORD_KEY = 'ucmid'
    # JWT_PASSWORD_ENCODE_ENCODING = 'UTF-8'


class DevelopmentConfig(Config):
    ABC = "abc_dev"
    ZTGG_DOMAIN = os.environ.get('ZTGG_DOMAIN')
    MONGO_PORT = 30001
    MONGO_URL = 'mongodb://{}:{}/'.format(ZTGG_DOMAIN, MONGO_PORT)


class ProductionConfig(Config):
    ABC = "abc_prod"

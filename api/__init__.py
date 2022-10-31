from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api

from bson import ObjectId
from marshmallow import fields

from config import Config, DevelopmentConfig, ProductionConfig

import logging
from logging.handlers import RotatingFileHandler

import os

logger = logging.getLogger(__name__)
restApp = Flask(__name__)
CORS(restApp)

restApi = Api(restApp)


def setConfig(restApp):
    running_env = os.environ.get("RUN_ENV") or "local"
    logger.info("The env is set as {}".format(running_env))
    if running_env == "development":
        restApp.config.from_object(DevelopmentConfig)
    elif running_env == "production":
        restApp.config.from_object(ProductionConfig)
    else:
        restApp.config.from_object(Config)

    os.makedirs(os.path.join("logs"), exist_ok=True)


setConfig(restApp)

if restApp.debug:
    file_handler = RotatingFileHandler('logs/cst-ui-api.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(restApp.config['LOGGING_LEVEL'])
    restApp.logger.addHandler(file_handler)

    restApp.logger.setLevel(restApp.config['LOGGING_LEVEL'])

from api.database.mondb import MonDBHandler
db = MonDBHandler(restApp)
# dchandler = DockerClientHandler(restApp)
# kubeHandler = KubeClientHandler(restApp)

ma = Marshmallow(restApp)
ma.Schema.TYPE_MAPPING[ObjectId] = fields.Str()


def add_res(curApi):
    from api.resources.user_api import UserApi
    curApi.add_resource(UserApi,
                        '{}user'.format(restApp.config['APPLICATION_ROOT']),
                        '{}user/<string:uname>'.format(
                            restApp.config['APPLICATION_ROOT']),
                        '{}user/<int:id>'.format(
                            restApp.config['APPLICATION_ROOT'])
                        )

    from api.resources.users_api import UsersApi
    curApi.add_resource(UsersApi,
                        '{}users'.format(restApp.config['APPLICATION_ROOT'])
                        )


add_res(restApi)

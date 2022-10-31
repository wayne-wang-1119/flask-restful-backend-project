from flask_restful import Resource
import logging

logger = logging.getLogger(__name__)


class UsersApi(Resource):
    def get(self):
        from api.daos.userDAO import UserDAO
        u_dao = UserDAO()
        return u_dao.findAllResources({})

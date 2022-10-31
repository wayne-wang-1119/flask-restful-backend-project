from flask_restful import Resource, request
from http import HTTPStatus
from api.utils.common_utils import verify_field_in_res, get_ignorecase_regex
import logging

logger = logging.getLogger(__name__)


class UserApi(Resource):
    def get(self, uname=None):
        from api.daos.userDAO import UserDAO
        u_dao = UserDAO()
        return u_dao.findAllResources({"name": get_ignorecase_regex(uname)})

    def delete(self, id=None):
        from api.daos.userDAO import UserDAO
        u_dao = UserDAO()

        del_selector = {"id": int(id)}
        users = u_dao.findAllResources(del_selector)

        if users is None or len(users) <= 0:
            return {"rep_code": HTTPStatus.CONFLICT, "msg": "There is no user with [{}] on file".format(id)}, int(HTTPStatus.CONFLICT)
        ret = u_dao.deleteResourcesBySelector(del_selector)
        if ret is None:
            return {"rep_code": HTTPStatus.CONFLICT, "msg": "Delete unsuccessfully, there would be no user with [{}] on file".format(id)}, int(HTTPStatus.CONFLICT)
        return {"rep_code": HTTPStatus.OK, "msg": "The user has been deleted successfully"}, int(HTTPStatus.OK)

    def post(self):
        api_key = request.headers.get("api_key")

        user = request.get_json()

        need_verified_fields = ["name", "age"]
        if not verify_field_in_res(need_verified_fields, user):
            return {"rep_code": HTTPStatus.METHOD_NOT_ALLOWED, "msg": "Please provide {} fields in payload".format(need_verified_fields)}, int(HTTPStatus.METHOD_NOT_ALLOWED)

        from api.daos.userDAO import UserDAO
        u_dao = UserDAO()

        selector = {
            "name": get_ignorecase_regex(user["name"]),
            "age": int(user["age"])
        }
        ret = u_dao.insertOneResource(user, selector)
        if type(ret) is int and ret == 0:
            return {"rep_code": HTTPStatus.CONFLICT, "msg": "The user[{}] is duplicated".format(user)}, int(HTTPStatus.CONFLICT)

        return {"rep_code": HTTPStatus.CREATED, "msg": "The user[{}] is created successfully".format(user)}, int(HTTPStatus.CREATED)

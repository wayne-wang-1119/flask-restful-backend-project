import logging
from api.utils.common_utils import get_ignorecase_regex
from api.daos.abstractDAO import AbstractDAO

logger = logging.getLogger(__name__)

COLLECTION = 'user'


class UserDAO(AbstractDAO):
    def __init__(self, db_client=None):
        super().__init__(COLLECTION, db_client)

    def checkIfUserExistWithName(self, name):
        users = self.db.find_all({"name": get_ignorecase_regex(name)})
        return users is not None and len(users) > 0

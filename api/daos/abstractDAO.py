import abc
import logging
from api import db, restApp
from api.utils.class_utils import getSchemaCls

from api.utils.common_utils import current_milli_time

from api.daos.idCounterDAO import IDCounterDAO

id_counter_dao = IDCounterDAO()

logger = logging.getLogger(__name__)


class AbstractDAO(abc.ABC):
    def __init__(self, col, db_client=None):
        self.db = db_client if db_client else db
        self.col = col
        self.schema_cls = getSchemaCls(col)
        self.resource_schema = self.schema_cls()
        self.resources_schema = self.schema_cls(many=True)

    def findAllResources(self, selector):
        resources = self.db.find_all(self.col, selector)
        return self.resources_schema.dump(resources)

    def findAllResourcesWithOrderAndLimit(self, selector, sort, limit):
        resources = self.db.find_all(
            self.col, selector).sort(sort).limit(limit)
        return self.resources_schema.dump(resources)

    def findAllResourcesWithOrder(self, selector, orderBy):
        resources = self.db.find_all(self.col, selector).sort(orderBy)
        return self.resources_schema.dump(resources)

    def findAllResourcesWithProjectionAndOrder(self, selector, projection, orderBy):
        resources = self.db.find_all_with_projection(
            self.col, selector, projection).sort(orderBy)
        return self.resources_schema.dump(resources)

    def updateOneResourceById(self, res):
        if "id" not in res:
            return -1

        selector = {"id": res["id"]}

        update_elements = {}

        if isinstance(res, dict):
            for k, v in res.items():
                if v:
                    update_elements[k] = v

            update_elements["updatedInMS"] = current_milli_time()
            update_elements["updatedBy"] = restApp.config['DEFAULT_CREATOR']

        updator = {"$set": update_elements}

        return self.db.update(self.col, selector, updator)

    def upsertOneResource(self, res, selector, unset_fields=None):
        update_elements = {}

        if isinstance(res, dict):
            for k, v in res.items():
                if v or v == 0:
                    update_elements[k] = v

            update_elements["updatedInMS"] = current_milli_time()
            update_elements["updatedBy"] = restApp.config['DEFAULT_CREATOR'] if "updatedBy" not in res or res["updatedBy"] is None else res["updatedBy"]

        updator = {"$set": update_elements} if not unset_fields else {
            "$set": update_elements, "$unset": unset_fields}

        return self.db.upsert(self.col, selector, updator)

    def insertOneResource(self, res, selector):
        find_res = self.findAllResources(selector)

        if find_res is None or len(find_res) <= 0:
            now = current_milli_time()
            res["createdInMS"] = now
            res["updatedInMS"] = now
            res["id"] = id_counter_dao.getIdFromCounter(self.col)

            res["createdBy"] = res["createdBy"] if "createdBy" in res else restApp.config['DEFAULT_CREATOR']
            res["updatedBy"] = res["updatedBy"] if "updatedBy" in res else restApp.config['DEFAULT_CREATOR']

            print("Insert a resource of {} with payload".format(self.col))
            return self.db.create_one(self.col, res).inserted_id
        else:
            return 0

    def deleteOneResourceById(self, res):
        if "id" not in res:
            return -1

        selectorOnlyWithId = {"id": res["id"]}
        return self.deleteResourcesBySelector(selectorOnlyWithId)

    def deleteResourcesBySelector(self, del_selector):
        return self.db.delete_many(self.col, del_selector)

from pymongo import MongoClient, ReturnDocument
from api.utils.common_utils import current_milli_time
import gridfs
import logging

logger = logging.getLogger(__name__)


class MonDBHandler():
    def __init__(self, app, col=None):
        self.db_name = app.config["MONGO_DB_NAME"]
        mongo_url = app.config['MONGO_URL']
        logger.info("Initializing DB Handler with {}".format(mongo_url))
        self.client = MongoClient(mongo_url)
        self.db = self.client[self.db_name]
        if col is not None:
            self.set_col(col)

    def set_col(self, col):
        self.col = col

    def find_all(self, col, selector):
        return self.db[col].find(selector)

    def find_all_with_projection(self, col, selector, projection):
        return self.db[col].find(selector, projection)

    def create_many(self, col, models):
        return self.db[col].insert_many(models)

    def create_one(self, col, model):
        return self.db[col].insert_one(model)

    def delete_many(self, col, del_filter):
        return self.db[col].delete_many(del_filter)

    def upsert(self, col, res_filter, res_update):
        return self.db[col].find_one_and_update(
            filter=res_filter,
            update=res_update,
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

    def update(self, col, res_filter, res_update):
        res_update["$set"]["updatedInMS"] = current_milli_time()
        return self.db[col].find_one_and_update(
            filter=res_filter,
            update=res_update,
            upsert=False,
            return_document=ReturnDocument.AFTER,
        )

    def aggregate(self, col, pipeline):
        return self.db[col].aggregate(pipeline)

    def save_file(self, filename, contents):
        fs = gridfs.GridFS(self.db)
        return fs.put(contents, filename=filename) if contents else None

    def get_mongodb_client(self):
        return self.client

    # def get_db_name(self):
    #     return CONNECT_DB

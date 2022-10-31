from api import db

import logging

logger = logging.getLogger(__name__)

COLLECTION = 'seq_counter'


class IDCounterDAO(object):
    def __init__(self):
        self.db = db

    def getIdFromCounter(self, collectionType):
        ret = self.db.upsert(
            COLLECTION,
            {"colType": '{}_seq'.format(collectionType)},
            {'$inc': {'counter': 1}}
        )
        if ret is None:
            ret = self.db.upsert(
                COLLECTION,
                {"colType": '{}_seq'.format(collectionType)},
                {'$inc': {'counter': 1}}
            )

        return int(ret["counter"])

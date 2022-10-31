import importlib

schema_module = importlib.import_module('api.schema.schema')


def getSchemaCls(collectionName):
    schemaName = collectionName[0].upper()+collectionName[1:]+'Schema'
    return getattr(schema_module, schemaName)

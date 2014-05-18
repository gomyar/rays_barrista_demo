
from pymongo import Connection
from pymongo.helpers import bson


class MongoDB(object):
    def __init__(self, host='localhost', port=27017, dbname="barrista"):
        self.host = host
        self.port = port
        self.dbname = dbname
        self._mongo_connection = None

    def init_mongo(self):
        self._mongo_connection = Connection(self.host, self.port)

    def db(self):
        return getattr(self._mongo_connection, self.dbname)

    def _collection(self, name):
        return getattr(self.db(), name)

    def get_object(self, collection_name, object_id):
        obj_dict = self._collection(collection_name).find_one(
            bson.ObjectId(object_id))
        obj_dict['_id'] = str(obj_dict['_id'])
        return obj_dict

    def save_object(self, collection_name, object_data):
        return self._collection(collection_name).save(object_data)

    def find(self, collection_name, **search_fields):
        return list(self._collection(collection_name).find(search_fields))

    def find_one(self, collection_name, **search_fields):
        return self._collection(collection_name).find_one(search_fields)

    def object_exists(self, collection_name, object_id):
        return bool(self.find_one(collection_name,
            _id=bson.ObjectId(object_id)))

    def remove_object(self, collection_name, object_id):
        self._collection(collection_name).remove(bson.ObjectId(object_id))

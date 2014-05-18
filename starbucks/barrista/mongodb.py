
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

    def object_exists(self, collection_name, object_id_str):
        object_id = self._safe_build_object_id(object_id_str)
        return bool(self.find_one(collection_name, _id=object_id))

    def _safe_build_object_id(self, object_id_str):
        try:
            return bson.ObjectId(object_id_str)
        except:
            return None

    def remove_object(self, collection_name, object_id):
        self._collection(collection_name).remove(bson.ObjectId(object_id))

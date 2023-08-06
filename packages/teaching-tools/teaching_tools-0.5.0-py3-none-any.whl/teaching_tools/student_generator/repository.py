# Inspiration: https://tinyurl.com/2am2r7ga
import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create_collection(self, collection, overwrite=True):
        raise NotImplementedError

    @abc.abstractmethod
    def drop_collection(self, collection):
        raise NotImplementedError

    @abc.abstractmethod
    def find(self, collection, query=None):
        raise NotImplementedError

    @abc.abstractmethod
    def insert(self, collection, records, return_result=False):
        raise NotImplementedError

    @abc.abstractmethod
    def drop(self, collection, query, return_result=False):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, collection, query, new_vals, return_result=False):
        raise NotImplementedError


class MongoRepository(AbstractRepository):
    def __init__(self, client, db):
        self.client = client
        self.db = self.client[db]

    def create_collection(self, collection, overwrite=True):
        if collection in self.db.list_collection_names():
            if not overwrite:
                raise Exception(
                    f"Collection {collection} already exists. Choose another name, or set `overwrite` to `True`."
                )
            else:
                self.db[collection].drop()

        self.db.create_collection(collection)

    def drop_collection(self, collection):
        if collection in self.db.list_collection_names():
            self.db[collection].drop()

    def find(self, collection, query=None):
        if query is None:
            q = {}
        else:
            q = query
        return self.db[collection].find(q)

    def insert(self, collection, records, return_result=False):
        r = self.db[collection].insert_many(records)
        if return_result:
            return {
                "acknowledged": r.acknowledged,
                "inserted_ids": r.inserted_ids,
            }

    def drop(self, collection, query, return_result=False):
        r = self.db[collection].delete_many(query)
        if return_result:
            return {
                "acknowledged": r.acknowledged,
                "deleted_count": r.deleted_count,
            }

    def update(self, collection, query, new_vals, return_result=False):
        nv = {"$set": {new_vals}}
        r = self.db[collection].update_many(query, nv)
        if return_result:
            return {
                "acknowledged": r.acknowledged,
                "matched_count": r.matched_count,
                "modified_count": r.modified_count,
            }

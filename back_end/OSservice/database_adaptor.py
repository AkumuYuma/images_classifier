from pymongo import MongoClient


class Database():
    def __init__(self, uri, db_name):
        client = MongoClient(uri)
        self._db = client.db_name

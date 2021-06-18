from pymongo import MongoClient
import gridfs


class Database_adaptor():
    def __init__(self, host="localhost"):
        port = "27017"
        client = MongoClient("mongodb://" + host + ":" + port)
        self._db = client.images
        self._fs = gridfs.GridFS(client.images)


    def flagga(self, query, identificativo):
        """
            Flagga il primo oggetto che risponde alla query.
            :param: query -> query per il db
            :param: identificativo -> identificativo per flaggare
        """
        self._db.fs.files.update_one(query, { "$set": {"processing": identificativo}})

    def find_one(self, *args, **kwargs):
        return self._db.fs.files.find_one(*args, **kwargs)

    def get_file(self, *args, **kwargs):
        return self._fs.get(*args, **kwargs)

    def cancella_binari(self, obj_id):
        """
            cancella i binari obj_id
        """
        self._db.fs.chunks.delete_many({"files_id": obj_id})

    def unflagga(self, identificativo, operazione):
        """
            Unflagga il primo oggetto che risponde alla query.
            :param: identificativo -> identificativo per unflaggare
            :param: operazione -> Quale operazione va considerata svolta (processed/permaSaved)
        """
        self._db.fs.files.update_one({"processing": identificativo}, {
                                  "$set": {operazione: True}, "$unset": {"processing": 1}})


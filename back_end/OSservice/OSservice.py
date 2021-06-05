from pymongo import MongoClient
from random import uniform
import time


class Salvatore():

    def salva_immagine(self, image):
        pass


def demone():
    client = MongoClient("mongodb://localhost:27017")
    db = client.images
    while True:
        s = Salvatore()
        identificativo = uniform(0, 1000)
        # Flaggo il file come in processamento
        db.fs.files.update_one({"processed": True, "permaSaved": False}, {
                               "$set": {"processing": identificativo}})
        # Prendo il file facendo la query
        element = db.fs.files.find_one({"processing": identificativo})
        if element is not None:
            # print(element["_id"])
            print(f"Trovato un elemento da salvare...")
            # TODO salva immagine
            s.salva_immagine(element)
            print(f"Elemento salvato, aggiorno lo stato nel database e cancello il file")
            db.fs.chunks.delete_many({"files_id": element["_id"]})
            db.fs.files.update_one({"processing": identificativo}, {
                                   "$set": {"permaSaved": True}, "$unset": {"processing": 1}})
        time.sleep(1)





if __name__ == "__main__":
    demone()

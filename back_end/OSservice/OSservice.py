# Database
from pymongo import MongoClient
# Compreso in pymongo
import gridfs


from random import uniform
import time
from swift_adaptor import Swift_adaptor


def demone():
    client = MongoClient("mongodb://localhost:27017")
    db = client.images
    fs = gridfs.GridFS(client.images)
    while True:
        # Nota che le credenziali si aggiornano ogni mezzora, ma ogni secondo chiamo il costruttore
        # Della classe Swift_adaptor quindi non ci sono problemi perchè ogni secondo leggo il nuovo token
        swift = Swift_adaptor()
        # Creo un nuovo container (se esiste già non fa niente)
        nome_container = "immagini"
        swift.crea_container(nome_container)
        identificativo = uniform(0, 1000)
        # Flaggo il file come in processamento
        db.fs.files.update_one({"processed": True, "permaSaved": False}, {
                               "$set": {"processing": identificativo}})
        # Prendo il file facendo la query
        element = db.fs.files.find_one({"processing": identificativo})
        if element is not None:

            print(element)
            file = fs.get(element["_id"])
            print(f"Trovato un elemento da salvare...")
            # TODO salva immagine bene!
            swift.crea_oggetto(nome_container, element["filename"], file.read())
            print(f"Elemento salvato, aggiorno lo stato nel database e cancello il file")
            db.fs.chunks.delete_many({"files_id": element["_id"]})
            db.fs.files.update_one({"processing": identificativo}, {
                                   "$set": {"permaSaved": True}, "$unset": {"processing": 1}})
        time.sleep(1)

if __name__ == "__main__":
    demone()

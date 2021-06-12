# Database
from pymongo import MongoClient
# Compreso in pymongo
import gridfs


from random import uniform
import time
from swift_adaptor import Swift_adaptor


def demone():
    print("Connessione con il client del db in corso...")
    client = MongoClient("mongodb://localhost:27017")
    db = client.images
    fs = gridfs.GridFS(client.images)
    print("Connessione riuscita")
    while True:
        # Nota che le credenziali si aggiornano ogni mezzora, ma ogni secondo chiamo il costruttore
        # Della classe Swift_adaptor quindi non ci sono problemi perchè ogni secondo leggo il nuovo token
        swift = Swift_adaptor()
        # Creo un nuovo container (se esiste già non fa niente)
        nome_container = "immagini"
        swift.crea_container(nome_container)

        # Flaggo il file come in processamento
        identificativo = uniform(0, 1000)
        db.fs.files.update_one({"processed": True, "permaSaved": False}, {
                               "$set": {"processing": identificativo}})
        # Prendo il file facendo la query
        element = db.fs.files.find_one({"processing": identificativo})
        # Se c'è almeno un file
        if element is not None:
            print(element)
            file = fs.get(element["_id"])
            print(f"Trovato un elemento da salvare...")

            # TODO Capire se funziona e aggiungere metadati
            # swift.crea_oggetto(nome_container, element["filename"], file.read())
            # print(f"Elemento salvato, aggiorno lo stato nel database e cancello il file")
            # db.fs.chunks.delete_many({"files_id": element["_id"]})

            print("Scrivo l'oggetto su file")
            with open(element["filename"], "wb") as outputfile:
                outputfile.write(file.read())
            print("File salvato in locale")

            db.fs.files.update_one({"processing": identificativo}, {
                                   "$set": {"permaSaved": True}, "$unset": {"processing": 1}})

        time.sleep(1)

if __name__ == "__main__":
    demone()

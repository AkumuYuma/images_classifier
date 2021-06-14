# Database
from pymongo import MongoClient
# Compreso in pymongo
import gridfs


from random import uniform
import time
from swift_utilities.swift_adaptor import Swift_adaptor


def demone():
    print("Connessione con il client del db in corso...")
    host = "localhost"
    port = "27017"
    client = MongoClient("mongodb://" + host + ":" + port)
    db = client.images
    fs = gridfs.GridFS(client.images)
    print("Connessione riuscita")
    print("Cerco file analizzati da salvare...")
    while True:
        # Nota che le credenziali si aggiornano ogni mezzora, ma ogni secondo chiamo il costruttore
        # Della classe Swift_adaptor quindi non ci sono problemi perchè ogni secondo leggo il nuovo token
        swift = Swift_adaptor()
        nome_container = "immagini"
        # Se il contaniner esiste già non faccio niente, altrimenti lo creo
        try:
            _ = swift.get_info_container(nome_container)
            print("Il container esiste")
        except:
            print("Il container non esiste, lo creo")
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
            print("Trovato un elemento analizzato da salvare")

            # with open(element["filename"], "wb") as f:
            #     f.write(file.read())

            # with open(element["filename"], "rb") as f:
            swift.crea_oggetto(nome_container, element["filename"], file.read(), headers = {"classification": element["classification"]})

            # TODO Capire se funziona e aggiungere metadati
            print(swift.info_oggetto(nome_container, element["filename"])[0])

            print("Elemento salvato su swift, aggiorno lo stato nel database e cancello il file")
            db.fs.chunks.delete_many({"files_id": element["_id"]})
            db.fs.files.update_one({"processing": identificativo}, {
                                  "$set": {"permaSaved": True}, "$unset": {"processing": 1}})
        swift.close_conn()
        time.sleep(1)

if __name__ == "__main__":
    demone()

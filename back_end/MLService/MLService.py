# Per connesione al db
from pymongo import MongoClient
# Per il demone
import time


# Classe analizzatore
from random import randint

class Analizzatore():
    def __init__(self):
        # Esempio di classi
        self._classi = [
            "bambino",
            "albero",
            "casa",
            "semaforo",
            "lampione"
        ]

    def predict(self, image):
        # Esempio di analisi
        delay_time = randint(0, 3)
        # Aspetto un tempo tra 0 e 3 secondi
        time.sleep(delay_time)
        classe = randint(0, len(self._classi) - 1)
        return self._classi[classe]


# TODO Usare l'URI del db come variabile di enviroment
# TODO Usare anche qui l'adattatore del db
def demone():
    analizzatore = Analizzatore()
    # Prendo il client del db
    client = MongoClient("mongodb://localhost:27017")
    # Prendo il db
    db = client.images
    while True:
        # Flaggo il file come in processamento
        db.fs.files.update_one({"processed": False}, {"$set": {"processing": True}})
        # Prendo il file facendo la query
        element = db.fs.files.find_one({"processing": True})
        # print(element)
        if element is not None:
            print(f"Trovato un elemento in analisi...")
            # Faccio la predizione
            classe = analizzatore.predict(element)
            print(f"Elemento analizzato, aggiorno lo stato nel database...")
            # Aggiorno il file dicendo che è stato processato ed elimino la flag di processamento
            # Aggiorno anche il campo classe
            db.fs.files.update_one({"processing": True}, {"$set": {"processed": True, "classification": classe}, "$unset": {"processing": 1}})

        # Faccio il fetch ogni secondo
        time.sleep(1)





if __name__ == "__main__":
    demone()

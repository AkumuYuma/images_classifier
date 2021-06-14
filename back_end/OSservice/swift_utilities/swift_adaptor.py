"""
    Adattatore per l'API di swift. Deve essere in grado di prendere il token e l'url dall'env del sist operativo e deve esporre
    metodi per salvare e recuperare immagini.
    Deve essere eseguito con permessi di root per poter accedere alla cartella /root e prendere i token
"""

import requests
import json
import swiftclient


def stampa_dizionario(dizionario):
    for el in dizionario:
        print(el + ": " + dizionario[el])



class Swift_adaptor():
    def __init__(self):
        # Leggo il token e l'url dai file nel sistema
        with open("/root/token_swift", "r") as f:
            os_token = f.readline()
            os_token = os_token.strip("\n")
        with open("/root/swift_url", "r") as f:
            os_storage_url = f.readline()
            os_storage_url = os_storage_url.strip("\n")
        self._swift = swiftclient.client.Connection(preauthurl = os_storage_url, preauthtoken = os_token)

    def stampa_info_account(self):
        """
            Stampa informazioni generiche sul OS. (Info sull'account e containers)
        """
        account = self._swift.get_account()
        print("")
        print("Info sull'account: ")
        stampa_dizionario(account[0])
        print("Lista dei container: ")
        print(account[1])
        print("")

    def stampa_info_container(self, nome_container):
        """
            Stampa info sul container. Se il container non esiste viene sollevata un'eccezione
        """
        print("")
        print("Faccio la richiesta al container...")
        container = self._swift.get_container(nome_container)
        stampa_dizionario(container[0])
        print("Oggetti nel container: ")
        print(container[1])
        print("")

    def get_info_container(self, nome_container):
        """
            ritorna il container nome_container
            response[0] contiene l'header del container
            response[1] contiene la lista con gli oggetti nel container
        """
        return self._swift.get_container(nome_container)

    def info_oggetto(self, nome_container, nome_oggetto):
        """
            Restituisce l'oggetto, se non esiste, viene sollevata un'eccezione
            il valore response[0] contiene gli headers (info) dell'oggetto
            il valore response[1] contiene il conenuto dell'oggetto
        """
        response = self._swift.get_object(nome_container, nome_oggetto)
        return response

    def crea_container(self, nome_container):
        """
            Crea un nuovo container con il nome passato
        """
        self._swift.put_container(nome_container)

    def crea_oggetto(self, nome_container, nome_oggetto, contenuto, headers = None):
        """
            Crea un nuovo oggetto nel container, conenuto deve essere un oggetto di tipo file.
        """
        self._swift.put_object(nome_container, nome_oggetto, contenuto, headers = None)

    def cancella_container(self, nome_container):
        """
            Cancella il container e tutto il suo contenuto
        """
        for image in self.get_info_container(nome_container)[1]:
            nome_immagine = image["name"]
            self.cancella_oggetto(nome_container, nome_immagine)
        self._swift.delete_container(nome_container)

    def cancella_oggetto(self, nome_container, nome_oggetto):
        """
            Cancella l'oggetto
        """
        self._swift.delete_object(nome_container, nome_oggetto)

    def close_conn(self):
        self._swift.close()


if __name__ == "__main__":
    ad = Swift_adaptor()
    ad.stampa_info_account()
    try:
        ad.get_info_container("ciccio")
    except:
        print("non c'e il container")

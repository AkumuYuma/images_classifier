"""
    Adattatore per l'API di swift. Deve essere in grado di prendere il token e l'url dall'env del sist operativo e deve esporre
    metodi per salvare e recuperare immagini.
    Deve essere eseguito con permessi di root per poter accedere alla cartella /root e prendere i token
"""

import requests
import json
import os
import subprocess

class Swift_adaptor():
    def __init__(self):
        # Leggo il token e l'url dai file nel sistema
        with open("/root/token_swift", "r") as f:
            self._os_token = f.readline()
            self._os_token = self._os_token.strip("\n")
        with open("/root/swift_url", "r") as f:
            self._os_storage_url = f.readline()
            self._os_storage_url = self._os_storage_url.strip("\n")
        self._auth_headers = { 'x-auth-token': self._os_token }

    def stampa_info_account(self):
        response = requests.get(self._os_storage_url, headers = self._auth_headers)
        # TODO debug
        print(response.json())

    def aggancia_container(self, nomeContainer):
        """
            Restituisce l'url del container, se non esiste lo crea
        """
        response = requests.get(self._os_storage_url + "/" + nomeContainer, headers = self._auth_headers, verify = False)
        print(response.json)



ad = Swift_adaptor()
ad.stampa_info_account()

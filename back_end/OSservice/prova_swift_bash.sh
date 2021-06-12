#!/bin/bash

export OS_TOKEN=$(cat /root/token_swift)
export OS_STORAGE_URL=$(cat /root/swift_url)


# Fa la richiesta per le info sull'account swift
curl -i "$OS_STORAGE_URL?format=json" -X GET -H "X-Auth-Token: $OS_TOKEN"
echo


# Stampa le info sul container immagini
curl -i "$OS_STORAGE_URL/immagini?format=json" -X GET -H "X-Auth-Token: $OS_TOKEN"
echo

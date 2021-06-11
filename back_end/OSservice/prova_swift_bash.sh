#!/bin/bash

export OS_TOKEN=$(cat /root/token_swift)
export OS_STORAGE_URL=$(cat /root/swift_url)


curl -i "$OS_STORAGE_URL?format=json" -X GET -H "X-Auth-Token: $OS_TOKEN"

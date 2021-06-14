#!/bin/bash

docker-compose --project-name applicazione down
docker-compose --project-name applicazione up -d

# Parto dall'immagine di node
FROM node:latest AS build
# Definisco una workdir
WORKDIR /app
# Copio i pacchetti per installare le dipendenze
COPY package*.json ./
# Installo le dipendenze
RUN npm install --production
# Copio tutto il contenuto della cartella
COPY . .
# Cambio l'host per raggiungere il backend (tramite il discovery network di docker-compose)
# RUN sed -i 's/localhost/backend/' ./src/components/FileHandler.js
# Faccio la build dell'app
RUN npm run build


FROM nginx:latest
WORKDIR /app
# Aggiorno la configurazione di nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
# Copio la build dell'app
COPY --from=build /app/build .

# Parto dall'immagine di node
FROM node:latest
# Definisco una workdir
WORKDIR /app
# Copio i pacchetti per installare le dipendenze
COPY package*.json ./
# Installo le dipendenze
RUN npm install --production && npm install -g serve
# Copio tutto il contenuto della cartella
COPY . .
# Faccio la build dell'app
RUN npm run build
# NOTA: Dopo gli ultimi due comandi, l'immagine contiene l'intera app già buildata.
#       Basta runnare l'immagine per servire il front end
#
# Espongo la porta su cui servire l'app
EXPOSE 80
# Do il comando serve
CMD serve -s build -l 80

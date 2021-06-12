# Dockerfile per buildare il servizio di main api
# Parto da python3
FROM python:latest
# Work directory
WORKDIR /app
# Prendo i requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copio tutta la cartella
COPY . .
# Espongo la porta su cui ascoltare
EXPOSE 443
# Faccio partire flask
CMD [ "python", "./app.py"]

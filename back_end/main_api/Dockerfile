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
# Cambio l'ip dell'host nell'app.
# In questo modo l'app cercherà di connettersi all'ip db fornito dal dns di docker-compose.
RUN sed -i 's/localhost/db/' ./app.py
# Espongo la porta su cui ascoltare
EXPOSE 443
# Faccio partire flask
CMD gunicorn -b 0.0.0.0:443 app:app

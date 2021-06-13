# Dockerfile per buildare il servizio di main api
# Parto da python3
FROM python:latest
# Work directory
WORKDIR /MachineLearning
# Prendo i requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copio tutta la cartella
COPY . .
# Cambio l'ip dell'host nell'app.
# In questo modo l'app cercherà di connettersi all'ip db fornito dal dns di docker-compose.
RUN sed -i 's/localhost/db/' ./MLService.py
# Faccio partire il demone
CMD python ./MLService.py

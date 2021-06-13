# images_classifier
Progetto di computing technologies


Per ogni servizio c'è un Dockerfile che builda l'immagine per il commit. Ogni volta che viene effettuata una modifica o un aggiornamento
su uno dei servizi, è necessario ribuildare l'immagine usando il dockerfile. (In particolare si può usare lo script rebuild.sh)
$ sudo ./rebuild.sh NOMEIMMAGINE

Le immagini buildate sono disponibili sul dockerhub akumuyuma e sono:
    akumuyuma/front_end
    akumuyuma/backend
    akumuyuma/mlservice
    akumuyuma/osservice
È stata anche utilizzata un'immagine base mongo per il database.

Nella cartella è anche presente un docker-compose.yml. Questo permette di costruire l'intero servizio. Fa partire tutti i servizi contemporaneamente
e produce un overlay network per permettere ai diversi servizi di comunicare utilizzando il loro nome (quello definito in docker-compose.yml).
In realtà la necessità è che ogni servizio possa accedere al servizio di database. In questo caso l'accesso verrà effettuato usando l'URI:
"mongodb://db:27017".
Nel source code al posto di db c'è localhost, dato che nella fase di developement abbiamo eseguito tutti i processi non dockerizzati.
Per lo stesso motivo all'interno di tutti i Dockerfile c'è la linea "RUN sed -i 's/localhost/db/' ./NOMESCRIPT". In questo modo, il cambiamento del nome
è stato effettuato solamente all'interno dell'immagine.

Per far partire l'intero servizio è quindi possibile usare docker-compose up (c'è lo script start_app.sh che fa questo) e per stoppare stop_app.sh.

In questo modo ogni parte del processo è stata automatizzata, in ottica devOps.

Ricapitolando, il workflow è:
    Modifica di una parte di codice
    run dello script per il rebuild dell'immagine
    run dello script per il restart dell'applicazione
    upload dell'immagine modificata su dockerhub
    upload del nuovo codice su github

Con questo procedimento è anche possibile aggiungere un ulteriore servizio in maniera trasparente. Basterà produrre un'immagine, modificare il file docker-compose
e restartare l'app.

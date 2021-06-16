# <img src="front_end/public/favicon.ico" width="40px" height="40px"> EikonApp 
## Introduzione
EikonApp è una web app per l'analisi di immagini tramite algoritmi di machine learning con un'architettura orientata ai microservizi pensata per supportare utenze elevate tramite l'utilizzo di tecnologie di cloud computing. La progettazione dell'architettura e lo sviluppo dell'app rappresentano il progetto di fine corso dell'esame di Computing Technologies (Laurea magistrale in Fisica con curriculum Particle Astroparticle Physics and Advanced Technologies UniBa). In particolare per il deployment sono state utilizzare risorse di ReCaS nella forma di Infrastracture as a Service. 

Lo schema implementativo dell'applicazione è mostrato di seguito: 

![Schema](media_readme/Schema_progetto.png) 

L'idea è che l'utente possa caricare immagini dal front end (o direttamente dall'api) e ricevere il risultato dell'analisi in tempo reale tramite una query dello stato di processamento. Nel caso in cui l'analisi richieda un tempo eccessivo o il servizio di ML sia irragiungibile, l'utente è in grado di lasciare un indirizzo email e il risultato viene inviato automaticamente alla conclusione del processamento. I file caricati, insieme ai relativi metadati ed alle informazioni sullo stato di processamento sono salvate su un database (si è scelto MongoDB). I servizi di Machine Learning e Object Storage fanno polling continuo in cerca di file successivi da analizzare e salvare. Lo storage persistente è stato aggiunto in ottica di retraining periodico del classificatore. Per evitare colli di bottiglia, dopo il salvataggio in cloud di un'immagine il servizio di object storage procede all'eliminazione del file binario nel database (ma non dei metadati). 
I vari servizi comunicano tra loro tramite l'overlay network messo a disposizione da docker-compose. Si prevede la necessità di migrare a servizi più sofisticati come docker-swarm per una maggiore granularità dei servizi e resilienza (per maggiori informazioni vedi [Dockerizzazione](#dockerizzazione)
Tutti i servizi vengono disaccoppiati il più possibile dalla tecnologia di cloud tramite adattatori software. 

Attualmente la parte di front end è servita all'indirizzo http://90.147.170.229, mentre l'api è servita su http://90.147.170.229:443. Di seguito una demo sul funzionamento attuale. 

![Funzionmento](media_readme/GIF_sito.gif) 

## Dockerizzazione
Ogni servizio è stato isolato all'interno di un container. In particolare sono state buildate immagini Docker che contengono tutto il necessario per eseguire l'istanza del servizio e dunque per mettere in produzione l'app basta pullare le immagini e comporle con un orchestratore. 
Attualmente le immagini sono disponibili all'indirizzo https://hub.docker.com/u/akumuyuma. 
In particolare esse sono: 
-   akumuyuma/front_end
-   akumuyuma/backend
-   akumuyuma/mlservice
-   akumuyuma/osservice

Ovviamente a questo si aggiunge l'immagine **mongo** utilizzata "as is" in quanto non richiedeva alcuna personalizzazione. 
Vediamo un esempio di build delle immagini. Il seguente è il Dockerfile per il front end.
```Dockerfile
FROM node:latest AS build
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
RUN npm run build


FROM nginx:latest
WORKDIR /app
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build .
```
In particolare questa è una multi stage build: quando viene buildata, vengono create due immagini, una a partire da node che installa le dipendenze e builda il frontend, la seconda a partire da nginx, che contiene solo l'app già buildata e la serve sulla porta 80. L'immagine *akumuyuma/front_end* caricata su dockerhub contiene solo la seconda immagine (quella a partire da nginx) più leggera e portabile. 

Si noti in (quasi) tutti i Dockerfile la presenza della riga `RUN sed -i 's/localhost/NUOVO_NOME/' ./NOME_FILE`, necessaria a cambiare solo all'interno dell'immagine l'indirizzo a cui vengono fatte le richieste, da localhost (utilizzato nella fase di developement) al nome del servizio specificato nel file docker-compose. 
Ad esempio, per l'accesso al database, anzichè fare la richiesta a `mongodb://localhost:27017` è necessario fare la richiesta a `mongodb://db:27017`, questa sostituzione viene fatta nel build context dell'immagine (ed in particolare aggiunge un layer). 

### Composizione dei docker
I diversi servizi sono stati poi orchestrati utilizzando docker compose. 
``` yml
version: "3.7"
services:
  front_end:
    image: akumuyuma/front_end:1.2
    ports:
      - 80:80
  backend:
    image: akumuyuma/backend:1.2
    ports:
      - 443:443

  db:
    image: mongo:latest
    volumes:
      - /data/progetto/mongoDB/database:/data/db
    ports:
      - 27017:27017

  mlservice:
    image: akumuyuma/mlservice:1.0

  osservice:
    image: akumuyuma/osservice:1.0
    volumes:
      - /root:/root
```
Tramite il comando `docker-compose up` è possibile far partire l'intera app. L'utilizzo di docker-compose non è solo determinato dalla possibilità di automatizzare l'avvio e l'arresto dell'insieme di servizi, ma anche dalla necessità di avere un overlay network (virtuale) tra i docker per permettere la comunicazione reciproca. È più chiaro adesso il motivo per cui l'uri del database diventa `mongodb://db:27017`, questo è determinato dalla scelta del nome del servizio. 

Si noti inoltre che, grazie alla scelta di inserire il codice all'interno delle immagini in fase di build, non è necessario quasi mai montare parti del filesystem host nelle macchine virtuali. Eccezione è il servizio di Object Storage che necessita l'accesso ai file nella cartella /root. Questo costituirebbe una vulnerabilità se per qualche motivo l'isolamento del docker dovesse venire meno e  inoltre riduce la portabilità del servizio che attualmente può essere eseguito solo sulla macchina particolare che contiene il token per l'object storage. Una soluzione potrebbe essere quella di fare richiesta direttamente a swift per il refresh del token invece di leggerlo dal filesystem. 

## Workflow di developement sull'app 
Per aggiornare una parte dell'app il workflow è il seguente:
- Scrivere il codice
- Ribuildare l'immagine (o buildare una nuova versione) con `docker build`. Ogni servizio contiene uno script bash `rebuild.sh` che esegue semplicemente il rebuild prendendo come parametro il nuovo nome dell'immagine. 
- Modificare eventualmente il file di composizione dell'app e restartarla tramite docker compose. In docker_compose_utilities è presente uno script `restart_app.sh` che automatizza questa parte. 

Questo workflow, pur non essendo ottimizzato, permette l'aggiunta di un servizio in maniera (quasi) trasparente e automatizza parte della messa in produzione avvicinandosi di poco ad uno stile DevOps. Chiaramente quel paradigma risulta essere lontano mancando non solo l'automatizzazione, ma anche la presenza di una test unit che testi il codice prima della messa in produzione. 

## Analisi codice
Guardiamo brevemente la composizione delle diverse parti del codice dell'app. 
### Front end 
Questa parte rappresenta un'interfaccia comoda per l'utilizzo del servizio. Si tratta di una applicazione a singola pagina renderizzata dinamicamente tramite l'uso di React.js. 
La funzione triggerata dal tasto Upload Image è il seguente: 
```javascript
const handleSubmit = () => {

        if (selectedFile != null) {
            setFileId(0);
            setStatus(null);
            const fd = new FormData();
            fd.append(props.name, selectedFile);
            axios.post(apiPaths.baseUploadUrl + props.name, fd)
                .then(res => {
                    setFileId(res.data.id);
                })
                .catch(err => {
                    console.log(err);
                });
        }
    }
```
Viene creato un FormData che contiene il file da caricare sul database e viene fatta una richiesta POST all'API. La risposta del server (id con cui il nuovo file viene salvato nel database) viene salvata nella variabile di stato FileId. 

Alla query dello stato, invece, viene triggerata la funzione: 
```javascript
    const queryStatus = () => {
        // Gestione per richiesta dello stato di processamento
        if (fileId != null) {
            axios.get(apiPaths.baseQueryUrl + fileId)
                .then(res => {
                    setStatus(res.data);
                })
        }
    }
```
In questo caso, invece, viene fatta una richiesta get all'API chiedendo lo stato di processamento e salvataggio del file. Anche in questo caso viene utilizzata una variabile di stato per aggiornare il testo da renderizzare a schermo.

### Back end
Questa parte è stata sviluppata in python tramite l'utilizzo di Flask. Il servizio di API salva file sul database (e restituisce l'id univoco sul db) e ne chiede lo stato di processamento. 
```python
@app.route('/api/upload/input=<inputFile>', methods=["POST"])
def upload(inputFile):
    """
        Path per l'upload di un file mandato tramite richiesta POST.
        Il file viene salvato nel database Mongo.
        :param: immagine
        :return: json con id del file caricato
    """
    file = request.files[inputFile]
    if not file:
        abort(
            404,
            description="No file Selected"
        )
    fileId = database.save_image(file.filename, file, processed=False, permaSaved=False, classification=None)
    return jsonify({"id": str(fileId)})
```

```python 
@app.route('/api/get_state/id=<file_Id>')
def get_state(file_Id):
    """
        :param: fileId -> Id del file da controllare.
        :return: json con stato dell'oggetto, 404 se file inesistente
    """
    file_Id = database.type_conversion(file_Id)
    file_obj = database.find_one({"_id": file_Id})
    if not file_obj:
        abort(
            404,
            description="Invalid id"
        )
    res = {
        "processed": file_obj["processed"],
        "permaSaved": file_obj["permaSaved"],
        "classification": file_obj["classification"]
    }
    return jsonify(res)
```

Si noti che l'interfaccia con il database viene gestita tramite un adattatore.

### Machine Learning e Object storage 
Attualmente la parte di Machine learning è solamente simulata. La parte interessante condivisa da entrambi i servizi è il modo di accedere al database.
```python
identificativo = random.uniform(0, 1000)
db.fs.files.update_one({"processed": True, "permaSaved": False}, {
                               "$set": {"processing": identificativo}})
        # Prendo il file facendo la query
        element = db.fs.files.find_one({"processing": identificativo})
        # Se c'è almeno un file
        if element is not None:
            #
            #
            # Cose da fare con l'oggetto
            #
            #
            db.fs.files.update_one({"processing": identificativo}, {
                                  "$set": {"permaSaved": True}, "$unset": {"processing": 1}})
```
Potrebbero esserci diversi servizi o diverse istanze di un servizio a fare la query ad un file da analizzare o da salvare ed è necessario garantire l'atomicità del processo. Per fare questo il primo file trovato viene immediatamente flaggato come in processamento (l'unicità in questo caso è garantito dall'atomicità delle operazioni del database) tramite un id univoco (generato randomicamente). Successivamente le operazioni vengono effettuate sull'oggetto in processamento.

## Miglioramenti e criticità
EikonApp è comunque ancora in gran parte progettuale e necessita di diverse modifiche prima che possa essere messa in produzione. Di seguito alcuni dei principali problemi e necessità:
- Debug al servizio di object storage. In particolare testing dell'effettivo funzionamento e aggiunta di metadati ( come il risultato della classificazione).
- Aggiungere parte effettiva di machine learning, in questo momento si tratta di una semplice simulazione randomica in quanto interessava principalmente la progettazione e realizzazione dell'architettura. 
- Refactoring al codice, in particolare:
    - Utilizzo di un database adaptor per parti di ML e OS;
    - Utilizzo di variabili di ambiente per evitare hardcoding di dati e url;
- Aggiungere un load balancer all'inizio dell'api e più in generale migrare l'app ad una soluzione più scalabile (come docker swarm) 
- Miglioramento della connesione di rete tra il front end e l'API. In questo momento il servizio di front end si comporta come un qualsiasi programma facendo richieste all'api tramite l'url pubblico e non attraverso l'overlay network. Questa soluzione non è ottimale e necessita di una revisione. (In particolare il problema è legato alla gestione dei CORS per la renderizzazione delle risposte dell'API nel browser)
- Aggiunta del servizio di e-mail. Attualmente il servizio di risposta ritardata è solamente parte del progetto e andrebbe realizzato completamente.

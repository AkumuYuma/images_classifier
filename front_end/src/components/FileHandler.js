import {useState} from 'react';
import axios from 'axios';

// Base url dell'api:
// NOTA: Prima di andare in production bisogna salvare queste stringhe in env variables

const host = "90.147.170.229"
const baseUrl = "http://" + host + ":443"
// Dizionario per i path di base dell'api
const apiPaths = {
    baseUploadUrl: baseUrl + "/api/upload/input=",
    baseQueryUrl: baseUrl + "/api/get_state/id="
}


function FileHandler(props) {
    // Hooks per lo stato
    // File selezionato
    const [selectedFile, setSelectedFile] = useState(null);
    // id del file nel database
    const [fileId, setFileId] = useState(null);
    // stato del file nel database
    const [status, setStatus] = useState(null);


    const handleSubmit = () => {
        // Gestione Click su tasto upload
        // Invio l'immagine all'api
        if (selectedFile != null) {
            // Rimuovo lo stato precedente
            setStatus(null);
            const fd = new FormData();
            fd.append(props.name, selectedFile);
            axios.post(apiPaths.baseUploadUrl + props.name, fd)
                .then(res => {
                    // Aggiorno lo stato inserendo l'id ottenuto come risposta
                    setFileId(res.data.id);
                })
                .catch(err => {
                    console.log(err);
                });
        }
    }

    const queryStatus = () => {
        // Gestione per richiesta dello stato di processamento
        if (fileId != null) {
            axios.get(apiPaths.baseQueryUrl + fileId)
                .then(res => {
                    setStatus(res.data);
                })
        }
    }

    return (
        <>
            {/* Renderizzazione condizionale dell'immagine */}
            {selectedFile != null && (
                <img className="img-holder" alt="" src={URL.createObjectURL(selectedFile)} />
            )}

            {/* Input */}
            <input type="file" name={props.name} id="input-file" accept="image/*" onChange={event => {
                // Aggiorno il file selezionato
                if (event.target.files && event.target.files[0]) setSelectedFile(event.target.files[0]);
            }} />
            {/* Label per immagine al posto del tasto */}
            <div className="label">
                <label htmlFor="input-file" className="image-upload">
                    <figure>
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="17" viewBox="0 0 20 17">
                            <path d="M10 0l-5.2 4.9h3.3v5.1h3.8v-5.1h3.3l-5.2-4.9zm9.3 11.5l-3.2-2.1h-2l3.4 2.6h-3.5c-.1 0-.2.1-.2.1l-.8 2.3h-6l-.8-2.2c-.1-.1-.1-.2-.2-.2h-3.6l3.4-2.6h-2l-3.2 2.1c-.4.3-.7 1-.6 1.5l.6 3.1c.1.5.7.9 1.2.9h16.3c.6 0 1.1-.4 1.3-.9l.6-3.1c.1-.5-.2-1.2-.7-1.5z"></path>
                        </svg>
                    </figure>
                    {/* Questo è un alias per il bottone scegli. Scelgo la foto tramite l'immagine */}
                    {/*<i className="material-icons">add_photo_alternate</i> */}
                    Choose your file
                </label>
            </div>

            {/* Tasto per upload */}
            <button className="submit" onClick={handleSubmit}>Upload Image</button>
            {/* Renderizzazione condizionale dell'id dell'immagine */}
            {fileId != null && (
                <p>The file has been saved with id: {fileId} </p>
            )}

            {/* Tasto per query dello stato */}
            <button className="getStatus" onClick={queryStatus}>Query status</button>
            <div className="response">
                {/* Renderizzazione condizionale dello stato */}
                {status != null && (
                    <>
                        <p>Processed: {status.processed ? "Yes" : "No"}</p>
                        <p>Permanently stored: {status.permaSaved ? "Yes" : "No"}</p>
                    </>
                )}
                {status != null && status.classification != null && (
                    <p>Predizione: {status.classification}</p>
                )}
            </div>
        </>
    );
}


export default FileHandler;

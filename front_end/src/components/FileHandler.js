import {useState} from 'react';
import axios from 'axios';

// Base url dell'api:
// NOTA: Prima di andare in production bisogna salvare queste stringhe in env variables
const baseUrl = "http://localhost:5000"
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
                <img className="img-holder" src={URL.createObjectURL(selectedFile)} />
            )}

            {/* Input */}
            <input type="file" name={props.name} id="input-file" accept="image/*" onChange={event => {
                // Aggiorno il file selezionato
                if (event.target.files && event.target.files[0]) setSelectedFile(event.target.files[0]);
            }} />
            {/* Label per immagine al posto del tasto */}
            <div className="label">
                <label htmlFor="input-file" className="image-upload">
                    {/* Questo è un alias per il bottone scegli. Scelgo la foto tramite l'immagine */}
                    <i className="material-icons">add_photo_alternate</i>
                    Choose your photo
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
            {/* Renderizzazione condizionale dello stato */}
            {status != null && (
                <div>
                    <p>Processato: {status.processed ? "Si" : "No"}</p>
                    <p>Salvato nello storage: {status.permaSaved ? "Si" : "No"}</p>
                </div>
            )}
            {status != null && status.classification != null && (
                <p>Predizione: {status.classification}</p>
            )}
        </>
    );
}


export default FileHandler;

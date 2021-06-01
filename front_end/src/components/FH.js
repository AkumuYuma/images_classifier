import {useState, useContext, createContext} from 'react';
import axios from 'axios';

// Dizionario per i path di base dell'api

const baseUrl = "http://localhost:5000"

const apiPaths = {
    baseUploadUrl: baseUrl + "/api/upload/input=",
    baseQueryUrl: baseUrl + "/api/get_state/id="
}

function CondImg(props) {
    // Necessaria per la renderizzazione condizionale dell'immagine
    if (props.src == null) return null
    return <img className={props.className} src={props.src} alt="" />
}


function RenderStatus(props) {
    // Renderizzazione condizionale della risposta (analizzato/non analizzato)
    if (props.selectedFile == null) return null;
    if (props.analyzed) {
        return <p className={props.className}>Your file has been analyzed!</p>;
    } else {
        return <p className={props.className}>Your file has not been analyzed yet!</p>;

    }
}


function FileHandler(props) {

    const [selectedFile, setSelectedFile] = useState(null);
    const [fileId, setFileId] = useState(null);
    const [analyzed, setAnalyzed] = useState(false);

    const handleSubmit = () => {
        // Gestione Click su tasto upload
        // Invio l'immagine all'api
        if (selectedFile != null) {
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
        if (fileId != null) {
            axios.get(apiPaths.baseQueryUrl + fileId)
                .then(res => {
                    setAnalyzed(res.data.processed);
                })
        }
    }

    return (
        <div>
            <CondImg className="img-holder" src={(selectedFile != null) ? URL.createObjectURL(selectedFile) : null} />
            <input type="file" name={props.name} id="input-file" accept="image/*" onChange={event => {
                // Aggiorno il file selezionato
                if (event.target.files && event.target.files[0]) setSelectedFile(event.target.files[0]);
            }} />
            <div className="label">
                <label htmlFor="input-file" className="image-upload">
                    {/* Questo è un alias per il bottone scegli. Scelgo la foto tramite l'immagine */}
                    <i className="material-icons">add_photo_alternate</i>
                    Choose your photo
                </label>
            </div>
            <button className="submit" onClick={handleSubmit}>Upload Image</button>
            {/*Stampa l'id nel db dell'oggetto appena caricato
                    TODO: Possibilità di query per lo stato del processamento.
                    */}
            <button className="getStatus" onClick={queryStatus}>Get Status</button>
            <RenderStatus className="response" selectedFile={selectedFile} analyzed={analyzed} />
        </div>
    );

}

export default FileHandler;

import React from 'react';
import axios from 'axios';

// Dizionario per i path di base dell'api
const apiPaths = {
    baseUploadUrl: "http://localhost:5000/api/upload/input="
}


class Image extends React.Component {
    // Componente per renderizzazione immagine
    // usa la proprietà image per scegliere l'immagine da renderizzare
    render() {
        if (this.props.image != null) {
            return <img className={this.props.className} src={this.props.image} id="target" alt="" />;
        } else {
            return null;
        }
    }
}


class FileHandler extends React.Component {
    // Componente per la gestione del caricamento del file
    constructor(props) {
        super(props);
        // Lo stato contiene sempre il file selezionato
        this.state = {
            selectedFile: null,
            selectedFileUrl: null,
            fileId: null
        };
        // Bind di this ai metodi
        this.fileSelectedHandler = this.fileSelectedHandler.bind(this);
        this.fileUploadHandler = this.fileUploadHandler.bind(this);
    }


    fileSelectedHandler(event) {
        // Gestione scelta del file
        // Se ho il file aggiorno lo stato
        if (event.target.files && event.target.files[0]) {
            this.setState({
                selectedFileUrl: URL.createObjectURL(event.target.files[0]),
                selectedFile: event.target.files[0],
                fileId: this.state.fileId
            })
        }
    }

    fileUploadHandler() {
        // Gestione Click su tasto upload
        // Invio l'immagine all'api
        if (this.state.selectedFile != null) {
            const fd = new FormData();
            fd.append(this.props.name, this.state.selectedFile);
            axios.post(apiPaths.baseUploadUrl + this.props.name, fd)
                .then(res => {
                    // Aggiorno lo stato inserendo l'id ottenuto come risposta
                    this.setState({
                        selectedFile: this.state.selectedFile.selectedFile,
                        selectedFileUrl: this.state.selectedFileUrl,
                        fileId: res.data.id
                    });
                })
                .catch(err => {
                    console.log(err);
                });
        }
    }

    render() {
        return (
            <div>
                <Image className="img-holder" image={this.state.selectedFileUrl} />
                <input type="file" name={this.props.name} id="input-file" accept="image/*" onChange={this.fileSelectedHandler} />
                <div className="label">
                    <label htmlFor="input-file" className="image-upload">
                        {/* Questo è un alias per il bottone scegli. Scelgo la foto tramite l'immagine */}
                        <i className="material-icons">add_photo_alternate</i>
                        Choose your photo
                    </label>
                </div>
                <button className="submit" onClick={this.fileUploadHandler}>Upload Image</button>
                {/*Stampa l'id nel db dell'oggetto appena caricato
                    TODO: Possibilità di query per lo stato del processamento.
                    TODO: Barra di avanzamento dell'upload
                */}
                <p className="objectId">{this.state.fileId}</p>
            </div>
        );
    }
}

export default FileHandler;

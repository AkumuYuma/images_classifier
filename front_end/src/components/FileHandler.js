import React from 'react';

class Image extends React.Component {
    render() {
        if (this.props.image != null) {
            return <img className={this.props.className} src={this.props.image} id="target" alt="" />;
        } else {
            return null;
        }
    }
}


class FileHandler extends React.Component {
    constructor(props) {
        super(props);
        this.state = {selectedFile: null};
        this.fileSelectedHandler = this.fileSelectedHandler.bind(this);
        this.fileUploadHandler = this.fileUploadHandler.bind(this);
    }


    fileSelectedHandler(event) {
        if (event.target.files && event.target.files[0]) {
            this.setState({
                selectedFile: URL.createObjectURL(event.target.files[0])
            })
        }
    }

    fileUploadHandler() {
        // Code to send Image
    }

    render() {
        return (
            <div>
                <Image className="img-holder" image={this.state.selectedFile} />
                <input type="file" name="image-upload" id="input-file" accept="image/*" onChange={this.fileSelectedHandler} />
                <div className="label">
                    <label htmlFor="input-file" className="image-upload">
                        <i className="material-icons">add_photo_alternate</i>
                        Choose your photo
                    </label>
                </div>
                <button className="submit" onClick={this.fileUploadHandler}>Upload Image</button>
            </div>
        );
    }
}

export default FileHandler;

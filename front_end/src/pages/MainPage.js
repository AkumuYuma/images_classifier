import React from 'react';
import FileHandler from '../components/FileHandler'


class MainPage extends React.Component {
    render() {
        return (
            <div className="page">
                <div className="container">
                    <h1 className="heading">Add your image</h1>
                    <FileHandler />
                </div>
            </div>
        );
    }
}


export default MainPage;

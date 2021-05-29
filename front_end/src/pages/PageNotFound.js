import React from 'react';
import {Link} from 'react-router-dom'

class PageNotFound extends React.Component {
    render() {
        return (
            <div>
                <h1>404 Page not Found!</h1>
                <Link to="/">Torna alla pagina principale</Link>
            </div>
        );
    }
}

export default PageNotFound;

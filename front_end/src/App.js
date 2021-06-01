import './App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from 'react-router-dom';


import MainPage from './pages/MainPage';
import PageNotFound from './pages/PageNotFound';

const paths = {
    MainPage: "/",
    PageNotFound: "/404"
}


function App() {
    return (
        <Router>
            <Switch>
                <Route exact path={paths.MainPage} component={MainPage} />
                <Route exact path={paths.PageNotFound} component={PageNotFound} />
                <Redirect to={paths.PageNotFound} />
            </Switch>
        </Router>
    );
}

export default App;

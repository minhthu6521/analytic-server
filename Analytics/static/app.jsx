const Router = window.ReactRouterDOM.BrowserRouter;
const Route =  window.ReactRouterDOM.Route;
const Link =  window.ReactRouterDOM.Link;
const Prompt =  window.ReactRouterDOM.Prompt;
const Switch = window.ReactRouterDOM.Switch;
const Redirect = window.ReactRouterDOM.Redirect;

const NavBar = () => {
    return (
        <ul>
            <li><Link to="/dashboard" exact >Dashboard </Link></li>
            <li><Link to="/feedback" exact >Feedback</Link></li>
            <li><Link to="/jobstats" exact >Job Stats</Link></li>
        </ul>)
}


const PageLayout = () => {
    const changeTimeRange = () => {
        console.log(timerange.value)
    }
    return (
        <div>
            <NavBar />
            <Route path="/dashboard" exact render={(props) => (<GraphLayout {...props} api="/api/dashboard"/>)} />
            <Route path="/feedback" exact render={(props) => (<GraphLayout {...props} api="/api/feedback"/>)} />
            <select onChange={changeTimeRange} id="timerange">
                <option value="7">7 days</option>
                <option value="30">1 month</option>
                <option value="90">3 months</option>
            </select>
        </div>
    )
}



const App = () => {
    return (
        <Router>
            <PageLayout />
        </Router>)
    };

ReactDOM.render(<App />, document.getElementById("container"));

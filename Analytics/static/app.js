var Router = window.ReactRouterDOM.BrowserRouter;
var Route = window.ReactRouterDOM.Route;
var Link = window.ReactRouterDOM.Link;
var Prompt = window.ReactRouterDOM.Prompt;
var Switch = window.ReactRouterDOM.Switch;
var Redirect = window.ReactRouterDOM.Redirect;

var NavBar = function NavBar() {
    return React.createElement("ul", null, React.createElement("li", null, React.createElement(Link, { to: "/dashboard", exact: true }, "Dashboard ")), React.createElement("li", null, React.createElement(Link, { to: "/feedback", exact: true }, "Feedback")), React.createElement("li", null, React.createElement(Link, { to: "/jobstats", exact: true }, "Job Stats")));
};

var PageLayout = function PageLayout() {
    var changeTimeRange = function changeTimeRange() {
        console.log(timerange.value);
    };
    return React.createElement("div", null, React.createElement(NavBar, null), React.createElement(Route, { path: "/dashboard", exact: true, render: function render(props) {
            return React.createElement(GraphLayout, Object.assign({}, props, { api: "/api/dashboard" }));
        } }), React.createElement(Route, { path: "/feedback", exact: true, render: function render(props) {
            return React.createElement(GraphLayout, Object.assign({}, props, { api: "/api/feedback" }));
        } }), React.createElement("select", { onChange: changeTimeRange, id: "timerange" }, React.createElement("option", { value: "7" }, "7 days"), React.createElement("option", { value: "30" }, "1 month"), React.createElement("option", { value: "90" }, "3 months")));
};

var App = function App() {
    return React.createElement(Router, null, React.createElement(PageLayout, null));
};

ReactDOM.render(React.createElement(App, null), document.getElementById("container"));
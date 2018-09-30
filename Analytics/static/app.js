
var App = function App() {
    var changeTimeRange = function changeTimeRange() {
        console.log(timerange.value);
    };
    return React.createElement(
        "div",
        null,
        React.createElement(GraphLayout, null),
        React.createElement(
            "select",
            { onChange: changeTimeRange, id: "timerange" },
            React.createElement(
                "option",
                { value: "7" },
                "7 days"
            ),
            React.createElement(
                "option",
                { value: "30" },
                "1 month"
            ),
            React.createElement(
                "option",
                { value: "90" },
                "3 months"
            )
        )
    );
};

ReactDOM.render(React.createElement(App, null), document.getElementById("container"));


var App = function App() {
  return React.createElement(
    "div",
    { className: "logo", onClick: function onClick() {
        return goHome();
      } },
    React.createElement(
      "div",
      null,
      "Testing~~~~"
    )
  );
};

ReactDOM.render(React.createElement(App, null), document.getElementById("container"));
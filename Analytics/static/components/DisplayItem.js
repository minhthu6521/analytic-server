var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var DisplayItem = function (_React$Component) {
    _inherits(DisplayItem, _React$Component);

    function DisplayItem() {
        var _ref;

        var _temp, _this, _ret;

        _classCallCheck(this, DisplayItem);

        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = arguments[_key];
        }

        return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = DisplayItem.__proto__ || Object.getPrototypeOf(DisplayItem)).call.apply(_ref, [this].concat(args))), _this), _this.mapItem = function (obj) {
            if (obj["display_type"] === "line_chart") {
                return React.createElement(LineChart, { data: obj["data"], id: obj.id, key: obj.id });
            } else if (obj["display_type"] == "text") {
                return React.createElement(TextField, { data: obj["data"], id: obj.id, key: obj.id });
            }
        }, _temp), _possibleConstructorReturn(_this, _ret);
    }

    _createClass(DisplayItem, [{
        key: "render",
        value: function render() {
            var _this2 = this;

            var arrayOfItems = this.props.data["items"].map(function (obj) {
                return _this2.mapItem(obj);
            });
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "h4",
                    null,
                    this.props.data.title
                ),
                arrayOfItems
            );
        }
    }]);

    return DisplayItem;
}(React.Component);

var LineChart = function (_React$Component2) {
    _inherits(LineChart, _React$Component2);

    function LineChart() {
        var _ref2;

        var _temp2, _this3, _ret2;

        _classCallCheck(this, LineChart);

        for (var _len2 = arguments.length, args = Array(_len2), _key2 = 0; _key2 < _len2; _key2++) {
            args[_key2] = arguments[_key2];
        }

        return _ret2 = (_temp2 = (_this3 = _possibleConstructorReturn(this, (_ref2 = LineChart.__proto__ || Object.getPrototypeOf(LineChart)).call.apply(_ref2, [this].concat(args))), _this3), _this3.updateChart = function () {
            var chart_data = {
                type: "line",
                data: _this3.props.data,
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            };
            var ctx = document.getElementById(_this3.props.id).getContext('2d');
            var myChart = new Chart(ctx, chart_data);
        }, _temp2), _possibleConstructorReturn(_this3, _ret2);
    }

    _createClass(LineChart, [{
        key: "componentDidUpdate",
        value: function componentDidUpdate(prevProps) {
            if (!_.isEqual(this.props.data, prevProps.data)) {
                this.updateChart();
            }
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.updateChart();
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement("canvas", { style: { maxHeight: "400px", maxWidth: "800px" }, id: this.props.id });
        }
    }]);

    return LineChart;
}(React.Component);

var TextField = function (_React$Component3) {
    _inherits(TextField, _React$Component3);

    function TextField() {
        _classCallCheck(this, TextField);

        return _possibleConstructorReturn(this, (TextField.__proto__ || Object.getPrototypeOf(TextField)).apply(this, arguments));
    }

    _createClass(TextField, [{
        key: "render",
        value: function render() {
            var all_labels = this.props.data.datasets.map(function (obj) {
                return React.createElement(
                    "div",
                    null,
                    React.createElement(
                        "h4",
                        null,
                        obj["label"]
                    ),
                    React.createElement(
                        "span",
                        null,
                        obj["data"][0]
                    )
                );
            });
            return React.createElement(
                "div",
                null,
                all_labels
            );
        }
    }]);

    return TextField;
}(React.Component);
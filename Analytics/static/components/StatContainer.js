var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var plan = JSON.parse(document.getElementById("search_plan").innerText);
var api = $("#fetch-api").data("fetch_api");

var StatContainer = function (_React$Component) {
    _inherits(StatContainer, _React$Component);

    function StatContainer() {
        _classCallCheck(this, StatContainer);

        var _this = _possibleConstructorReturn(this, (StatContainer.__proto__ || Object.getPrototypeOf(StatContainer)).call(this));

        _this.updateData = function () {
            $.ajax({
                type: 'GET',
                url: _this.props.api,
                data: { data: JSON.stringify(_this.state.filter || {}) },
                success: function success(data) {
                    _this.setState({
                        data: data
                    });
                }
            });
        };

        _this.setFilter = function (id, value) {
            _this.setState({
                filter: Object.assign({}, _this.state.filter, _defineProperty({}, id, value))
            }, function () {
                _this.updateData();
            });
        };

        _this.state = {
            filter: {},
            data: []
        };
        return _this;
    }

    _createClass(StatContainer, [{
        key: "componentDidUpdate",
        value: function componentDidUpdate(prevProps, prevState) {
            console.log("didupdate", this.state.filter, prevState.filter);
            if (!_.isEqual(this.state.filter, prevState.filter)) {
                this.updateData();
            }
        }
    }, {
        key: "componentDidMount",
        value: function componentDidMount() {
            this.updateData();
        }
    }, {
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(FilterLayout, { plan: this.props.plan, setFilter: this.setFilter }),
                React.createElement(GraphLayout, { data: this.state.data })
            );
        }
    }]);

    return StatContainer;
}(React.Component);

ReactDOM.render(React.createElement(StatContainer, { plan: plan, api: api }), document.getElementById("stat_container"));
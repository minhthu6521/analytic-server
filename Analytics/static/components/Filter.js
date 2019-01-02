var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var DropdownFilter = function (_React$Component) {
    _inherits(DropdownFilter, _React$Component);

    function DropdownFilter() {
        var _ref;

        var _temp, _this, _ret;

        _classCallCheck(this, DropdownFilter);

        for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
            args[_key] = arguments[_key];
        }

        return _ret = (_temp = (_this = _possibleConstructorReturn(this, (_ref = DropdownFilter.__proto__ || Object.getPrototypeOf(DropdownFilter)).call.apply(_ref, [this].concat(args))), _this), _this.change = function (e) {
            _this.props.action(_this.props.data.id, e.target.value);
        }, _temp), _possibleConstructorReturn(_this, _ret);
    }

    _createClass(DropdownFilter, [{
        key: "render",
        value: function render() {
            var arrayOfOptions = this.props.data.context.options.map(function (obj) {
                return React.createElement(
                    "option",
                    { value: obj[0], key: obj[0] },
                    obj[1]
                );
            });
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "h3",
                    null,
                    this.props.data.context.title
                ),
                React.createElement(
                    "select",
                    { className: "form-control dropdown-widget", id: this.props.data.id, onChange: this.change },
                    arrayOfOptions
                )
            );
        }
    }]);

    return DropdownFilter;
}(React.Component);

var DatePicker = function (_React$Component2) {
    _inherits(DatePicker, _React$Component2);

    function DatePicker() {
        _classCallCheck(this, DatePicker);

        return _possibleConstructorReturn(this, (DatePicker.__proto__ || Object.getPrototypeOf(DatePicker)).apply(this, arguments));
    }

    _createClass(DatePicker, [{
        key: "render",
        value: function render() {
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "h3",
                    null,
                    this.props.data.context.title
                ),
                React.createElement("input", { type: "text", id: this.props.data.id, className: "form-control has-date-picker" })
            );
        }
    }]);

    return DatePicker;
}(React.Component);

var Select2Filter = function (_React$Component3) {
    _inherits(Select2Filter, _React$Component3);

    function Select2Filter(props) {
        _classCallCheck(this, Select2Filter);

        var _this3 = _possibleConstructorReturn(this, (Select2Filter.__proto__ || Object.getPrototypeOf(Select2Filter)).call(this, props));

        _this3.getCheckedValues = function () {
            var values = _this3.props.value;
            return _.isArray(values) ? values : [];
        };

        _this3.isSelected = function (value) {
            var selectedValues = _this3.getCheckedValues();
            return selectedValues.indexOf(value) >= 0;
        };

        _this3.getOnChangeHandler = function (e) {
            _this3.setState({ value: $(e.currentTarget).val() }, function () {
                _this3.props.action(_this3.props.data.id, _this3.state.value || []);
            });
        };

        _this3.state = {
            open: [],
            value: []
        };
        return _this3;
    }

    _createClass(Select2Filter, [{
        key: "toggleOpen",
        value: function toggleOpen() {
            this.setOpen(!this.state.open);
        }
    }, {
        key: "setOpen",
        value: function setOpen(open) {
            this.setState({ open: open });
            openCloseStore.setFilterState(this.props.name, open);
        }
    }, {
        key: "render",
        value: function render() {
            var open = this.state.open;


            var select2events = [['change.react-select2-wrapper', 'onChange'], ['select2:open.react-select2-wrapper', 'onOpen'], ['select2:close.react-select2-wrapper', 'onClose'], ['select2:select.react-select2-wrapper', 'onSelect'], ['select2:unselect.react-select2-wrapper', 'onUnselect']];

            var triangleStyle = {};
            if (!open) {
                triangleStyle.transform = 'rotate(-90deg)';
            }

            return React.createElement(
                "div",
                null,
                React.createElement(
                    "h3",
                    null,
                    this.props.data.context.title
                ),
                React.createElement(
                    "div",
                    { className: "filter-category-selections", ref: "selections" },
                    React.createElement(Select2Component, {
                        multiple: true,
                        data: this.props.data.context.options,
                        value: this.state.value,
                        events: select2events,
                        onChange: this.getOnChangeHandler,
                        isSelected: this.isSelected,
                        options: {
                            placeholder: "Start typing",
                            width: '100%',

                            allowClear: true
                        }
                    })
                )
            );
        }
    }]);

    return Select2Filter;
}(React.Component);

var CheckboxFilter = function (_React$Component4) {
    _inherits(CheckboxFilter, _React$Component4);

    function CheckboxFilter(props) {
        _classCallCheck(this, CheckboxFilter);

        var _this4 = _possibleConstructorReturn(this, (CheckboxFilter.__proto__ || Object.getPrototypeOf(CheckboxFilter)).call(this, props));

        _this4.change = function (e) {
            var options = [].concat(_toConsumableArray(_this4.state.options));
            var index = void 0;

            if (e.target.checked) {
                options.push(e.target.value);
            } else {
                index = options.indexOf(e.target.value);
                options.splice(index, 1);
            }

            // update the state with the new array of options
            _this4.setState({ options: options });
            _this4.props.action(_this4.props.data.id, options);
        };

        _this4.state = {
            options: []
        };
        return _this4;
    }

    _createClass(CheckboxFilter, [{
        key: "render",
        value: function render() {
            var _this5 = this;

            var arrayOfOptions = this.props.data.context.options.map(function (obj) {
                return React.createElement(
                    "div",
                    { className: "checkbox-field", key: obj[0] },
                    React.createElement("input", { id: obj[0], type: "checkbox", value: obj[0], name: _this5.props.data.id, onChange: _this5.change }),
                    React.createElement(
                        "label",
                        { htmlFor: obj[0] },
                        obj[1]
                    )
                );
            });
            return React.createElement(
                "div",
                null,
                React.createElement(
                    "h3",
                    null,
                    this.props.data.context.title
                ),
                arrayOfOptions
            );
        }
    }]);

    return CheckboxFilter;
}(React.Component);
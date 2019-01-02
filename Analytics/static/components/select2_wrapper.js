var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; };

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

// Derived from https://github.com/rkit/react-select2-wrapper at 4.10.2018
// The MIT License (MIT)
// Copyright (c) 2015 Igor Romanov

function _spread(obj, keys) {
    var target = {};
    for (var i in obj) {
        if (keys.indexOf(i) >= 0) continue;
        if (!Object.prototype.hasOwnProperty.call(obj, i)) continue;
        target[i] = obj[i];
    }
    return target;
}

// inlined from shallow-equal-fuzzy
var shallowEqualFuzzy = function () {
    // inlined http://underscorejs.org/ realization isString, isNumber
    var toString = Object.prototype.toString;

    function isString(obj) {
        return toString.call(obj) === "[object String]";
    }

    function isNumber(obj) {
        return toString.call(obj) === "[object Number]";
    }

    /**
     * inlined Object.is polyfill to avoid requiring consumers ship their own
     * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is
     */
    function is(x, y) {
        // SameValue algorithm
        if (x === y) {
            // Steps 1-5, 7-10
            // Steps 6.b-6.e: +0 != -0
            return x !== 0 || 1 / x === 1 / y;
        } else {
            // Step 6.a: NaN == NaN
            /* eslint no-self-compare: 0 */
            return x !== x && y !== y;
        }
    }

    function isFuzzy(x, y) {
        /* eslint eqeqeq: 0 */
        if (x == y) {
            if ((isString(x) || isNumber(x)) && (isString(y) || isNumber(y))) {
                return true;
            }
        }
        return is(x, y);
    }

    var hasOwnProperty = Object.prototype.hasOwnProperty;

    // custom algoritm from https://github.com/facebook/fbjs
    // fbjs/lib/shallowEqual
    function shallowEqualFuzzy(objA, objB) {
        if (isFuzzy(objA, objB)) {
            return true;
        }

        if ((typeof objA === "undefined" ? "undefined" : _typeof(objA)) !== "object" || objA === null || (typeof objB === "undefined" ? "undefined" : _typeof(objB)) !== "object" || objB === null) {
            return false;
        }

        if (objA instanceof Array && objB instanceof Array) {
            if (objA.length !== objB.length) {
                return false;
            }
            // greed search
            var valA,
                iLen = objA.length;
            var equalityMap = new Array(iLen);
            for (var i = 0; i < iLen; i++) {
                valA = objA[i];
                if (shallowEqualFuzzy(valA, objB[i])) {
                    // elements in array in normal order
                    equalityMap[i] = true;
                    continue;
                }

                // elements in array have different order
                var isEqual = false;
                for (var k = 0, kLen = objB.length; k < kLen; k++) {
                    if (equalityMap[k]) {
                        continue;
                    }
                    if (shallowEqualFuzzy(valA, objB[k])) {
                        equalityMap[k] = true;
                        isEqual = true;
                        break;
                    }
                }
                if (!isEqual) {
                    return false;
                }
            }
            return true;
        }

        var keysA = Object.keys(objA);
        var keysB = Object.keys(objB);

        if (keysA.length !== keysB.length) {
            return false;
        }

        for (var j = 0; j < keysA.length; j++) {
            if (!hasOwnProperty.call(objB, keysA[j]) || !shallowEqualFuzzy(objA[keysA[j]], objB[keysA[j]])) {
                return false;
            }
        }
        return true;
    }

    return shallowEqualFuzzy;
}();

var namespace = 'react-select2-wrapper';

var Select2Component = function () {
    var $el = null,
        initialRender = true,
        forceUpdateValue = false;
    /* default props to be always given: {
        data: [],
        events: [
            [`change.${namespace}`, 'onChange'],
            [`select2:open.${namespace}`, 'onOpen'],
            [`select2:close.${namespace}`, 'onClose'],
            [`select2:select.${namespace}`, 'onSelect'],
            [`select2:unselect.${namespace}`, 'onUnselect'],
        ],
        options: {}
        multiple: false,
    }; */

    var aSelect2Component = function (_React$Component) {
        _inherits(aSelect2Component, _React$Component);

        function aSelect2Component() {
            _classCallCheck(this, aSelect2Component);

            return _possibleConstructorReturn(this, (aSelect2Component.__proto__ || Object.getPrototypeOf(aSelect2Component)).apply(this, arguments));
        }

        _createClass(aSelect2Component, [{
            key: "componentDidMount",
            value: function componentDidMount() {
                this.initSelect2(this.props);
                this.updateValue();
            }
        }, {
            key: "componentWillReceiveProps",
            value: function componentWillReceiveProps(nextProps) {
                initialRender = false;
                this.updSelect2(nextProps);
            }
        }, {
            key: "componentDidUpdate",
            value: function componentDidUpdate(prevProps) {
                if (this.props.value !== prevProps.value) {
                    this.updateValue();
                }
            }
        }, {
            key: "componentWillUnmount",
            value: function componentWillUnmount() {
                this.destroySelect2();
            }
        }, {
            key: "initSelect2",
            value: function initSelect2(props) {
                var options = props.options;


                $el = $(ReactDOM.findDOMNode(this));
                // fix for updating selected value when data is changing
                if (forceUpdateValue) {
                    this.updateSelect2Value(null);
                }
                $el.select2(this.prepareOptions(options));
                this.attachEventHandlers(props);
            }
        }, {
            key: "updSelect2",
            value: function updSelect2(props) {
                var prevProps = this.props;

                if (!shallowEqualFuzzy(prevProps.data, props.data)) {
                    forceUpdateValue = true;
                    this.destroySelect2(false);
                    this.initSelect2(props);
                    return;
                }

                var options = props.options;

                if (!shallowEqualFuzzy(prevProps.options, options)) {
                    $el.select2(this.prepareOptions(options));
                }

                var handlerChanged = function handlerChanged(e) {
                    return prevProps[e[1]] !== props[e[1]];
                };
                if (props.events.some(handlerChanged)) {
                    this.detachEventHandlers();
                    this.attachEventHandlers(props);
                }
            }
        }, {
            key: "updateSelect2Value",
            value: function updateSelect2Value(value) {
                $el.off("change." + namespace).val(value).trigger('change');

                var onChange = this.props.onChange;
                if (onChange) {
                    $el.on("change." + namespace, onChange);
                    $el.select2('close');
                }
            }
        }, {
            key: "updateValue",
            value: function updateValue() {
                var _props = this.props,
                    value = _props.value,
                    defaultValue = _props.defaultValue,
                    multiple = _props.multiple;

                var newValue = this.prepareValue(value, defaultValue);
                var currentValue = multiple ? $el.val() || [] : $el.val();

                if (!this.fuzzyValuesEqual(currentValue, newValue) || forceUpdateValue) {
                    this.updateSelect2Value(newValue);
                    if (!initialRender) {
                        $el.trigger('change');
                    }
                    forceUpdateValue = false;
                }
            }
        }, {
            key: "fuzzyValuesEqual",
            value: function fuzzyValuesEqual(currentValue, newValue) {
                return currentValue === null && newValue === '' || shallowEqualFuzzy(currentValue, newValue);
            }
        }, {
            key: "destroySelect2",
            value: function destroySelect2() {
                var withCallbacks = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : true;

                if (withCallbacks) {
                    this.detachEventHandlers();
                }

                $el.select2('destroy');
                $el = null;
            }
        }, {
            key: "attachEventHandlers",
            value: function attachEventHandlers(props) {
                props.events.forEach(function (event) {
                    if (typeof props[event[1]] !== 'undefined') {
                        $el.on(event[0], props[event[1]]);
                    }
                });
            }
        }, {
            key: "detachEventHandlers",
            value: function detachEventHandlers() {
                var _this2 = this;

                this.props.events.forEach(function (event) {
                    if (typeof _this2.props[event[1]] !== 'undefined') {
                        $el.off(event[0]);
                    }
                });
            }
        }, {
            key: "prepareValue",
            value: function prepareValue(value, defaultValue) {
                var issetValue = typeof value !== 'undefined' && value !== null;
                var issetDefaultValue = typeof defaultValue !== 'undefined';

                if (!issetValue && issetDefaultValue) {
                    return defaultValue;
                }
                return value;
            }
        }, {
            key: "prepareOptions",
            value: function prepareOptions(options) {
                var opt = options;
                if (typeof opt.dropdownParent === 'string') {
                    opt.dropdownParent = $(opt.dropdownParent);
                }
                return opt;
            }
        }, {
            key: "isObject",
            value: function isObject(value) {
                var type = typeof value === "undefined" ? "undefined" : _typeof(value);
                return type === 'function' || value && type === 'object' || false;
            }
        }, {
            key: "makeOption",
            value: function makeOption(item, isSelected) {
                if (this.isObject(item)) {
                    var value = item.value;
                    var text = item.label;
                    var itemParams = _spread(item, ["value", "label"]);
                    return React.createElement(
                        "option",
                        Object.assign({ key: "option-" + value, value: value
                        }, itemParams),
                        text
                    );
                }

                return React.createElement(
                    "option",
                    { key: "option-" + item, value: item },
                    item
                );
            }
        }, {
            key: "render",
            value: function render() {
                var _this3 = this;

                var value = this.props.value;
                var data = this.props.data || [];
                var isSelected = this.props.isSelected;
                var props = _spread(this.props, ["value", "data", "isSelected"]);

                delete props.options;
                delete props.events;
                delete props.onOpen;
                delete props.onClose;
                delete props.onSelect;
                delete props.onChange;
                delete props.onUnselect;

                return React.createElement(
                    "select",
                    props,
                    data.map(function (item, k) {
                        if (_this3.isObject(item) && _this3.isObject(item.children)) {
                            var children = item.children;
                            var text = item.label;
                            var itemParams = _spread(item.itemParams, ["children", "text"]);
                            return React.createElement(
                                "optgroup",
                                Object.assign({ key: "optgroup-" + k, label: text }, itemParams),
                                children.map(function (child) {
                                    return _this3.makeOption(child, isSelected);
                                })
                            );
                        }
                        return _this3.makeOption(item, isSelected);
                    })
                );
            }
        }]);

        return aSelect2Component;
    }(React.Component);

    ;
    return aSelect2Component;
}();
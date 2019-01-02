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
var shallowEqualFuzzy = (function () {
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

        if (typeof objA !== "object" || objA === null || typeof objB !== "object" || objB === null) {
            return false;
        }

        if (objA instanceof Array && objB instanceof Array) {
            if (objA.length !== objB.length) {
                return false;
            }
            // greed search
            var valA, iLen = objA.length;
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
            if (!hasOwnProperty.call(objB, keysA[j]) ||
                !shallowEqualFuzzy(objA[keysA[j]], objB[keysA[j]])) {
                return false;
            }
        }
        return true;
    }

    return shallowEqualFuzzy
})();


const namespace = 'react-select2-wrapper';

var Select2Component = (function () {
    let $el = null, initialRender = true, forceUpdateValue = false;
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

    class aSelect2Component extends React.Component{

        componentDidMount() {
            this.initSelect2(this.props);
            this.updateValue();
        }

        componentWillReceiveProps(nextProps) {
            initialRender = false;
            this.updSelect2(nextProps);
        }

        componentDidUpdate(prevProps) {
            if (this.props.value !== prevProps.value) {
                this.updateValue();
            }
        }

        componentWillUnmount() {
            this.destroySelect2();
        }

        initSelect2(props) {
            const {options} = props;

            $el = $(ReactDOM.findDOMNode(this));
            // fix for updating selected value when data is changing
            if (forceUpdateValue) {
                this.updateSelect2Value(null);
            }
            $el.select2(this.prepareOptions(options));
            this.attachEventHandlers(props);
        }

        updSelect2(props) {
            const prevProps = this.props;

            if (!shallowEqualFuzzy(prevProps.data, props.data)) {
                forceUpdateValue = true;
                this.destroySelect2(false);
                this.initSelect2(props);
                return;
            }

            const {options} = props;
            if (!shallowEqualFuzzy(prevProps.options, options)) {
                $el.select2(this.prepareOptions(options));
            }

            const handlerChanged = e => prevProps[e[1]] !== props[e[1]];
            if (props.events.some(handlerChanged)) {
                this.detachEventHandlers();
                this.attachEventHandlers(props);
            }
        }

        updateSelect2Value(value) {
            $el.off(`change.${namespace}`).val(value).trigger('change');

            const onChange = this.props.onChange;
            if (onChange) {
                $el.on(`change.${namespace}`, onChange);
                $el.select2('close');
            }
        }

        updateValue() {
            const {value, defaultValue, multiple} = this.props;
            const newValue = this.prepareValue(value, defaultValue);
            const currentValue = multiple ? $el.val() || [] : $el.val();

            if (!this.fuzzyValuesEqual(currentValue, newValue) || forceUpdateValue) {
                this.updateSelect2Value(newValue);
                if (!initialRender) {
                    $el.trigger('change');
                }
                forceUpdateValue = false;
            }
        }

        fuzzyValuesEqual(currentValue, newValue) {
            return (currentValue === null && newValue === '') ||
                shallowEqualFuzzy(currentValue, newValue);
        }

        destroySelect2(withCallbacks = true) {
            if (withCallbacks) {
                this.detachEventHandlers();
            }

            $el.select2('destroy');
            $el = null;
        }

        attachEventHandlers(props) {
            props.events.forEach(event => {
                if (typeof props[event[1]] !== 'undefined') {
                    $el.on(event[0], props[event[1]]);
                }
            });
        }

        detachEventHandlers() {
            this.props.events.forEach(event => {
                if (typeof this.props[event[1]] !== 'undefined') {
                    $el.off(event[0]);
                }
            });
        }

        prepareValue(value, defaultValue) {
            const issetValue = typeof value !== 'undefined' && value !== null;
            const issetDefaultValue = typeof defaultValue !== 'undefined';

            if (!issetValue && issetDefaultValue) {
                return defaultValue;
            }
            return value;
        }

        prepareOptions(options) {
            const opt = options;
            if (typeof opt.dropdownParent === 'string') {
                opt.dropdownParent = $(opt.dropdownParent);
            }
            return opt;
        }

        isObject(value) {
            const type = typeof value;
            return type === 'function' || (value && type === 'object') || false;
        }

        makeOption(item, isSelected) {
            if (this.isObject(item)) {
                const value = item.value;
                const text = item.label;
                const itemParams = _spread(item, ["value", "label"]);
                return (<option key={`option-${value}`} value={value}
                                {...itemParams}>{text}</option>);
            }

            return (<option key={`option-${item}`} value={item}>{item}</option>);
        }

        render() {
            const value = this.props.value;
            const data = this.props.data || [];
            const isSelected = this.props.isSelected;
            var props = _spread(this.props, ["value", "data", "isSelected"]);

            delete props.options;
            delete props.events;
            delete props.onOpen;
            delete props.onClose;
            delete props.onSelect;
            delete props.onChange;
            delete props.onUnselect;

            return (
                <select {...props}>
                    {data.map((item, k) => {
                        if (this.isObject(item) && this.isObject(item.children)) {
                            const children = item.children;
                            const text = item.label;
                            const itemParams = _spread(item.itemParams, ["children", "text"]);
                            return (
                                <optgroup key={`optgroup-${k}`} label={text} {...itemParams}>
                                    {children.map((child) => this.makeOption(child, isSelected))}
                                </optgroup>
                            );
                        }
                        return this.makeOption(item, isSelected);
                    })}
                </select>
            );
        }
    };
    return aSelect2Component
})();

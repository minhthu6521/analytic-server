class DropdownFilter extends React.Component {
    change = (e) => {
        this.props.action(this.props.data.id, e.target.value);
    };

    render()  {
        var arrayOfOptions = this.props.data.context.options.map((obj) => {
            return (<option value={obj[0]} key={obj[0]}>{obj[1]}</option>)
        });
        return(<div>
            <h3>{this.props.data.context.title}</h3>
            <select className="form-control dropdown-widget" id={this.props.data.id} onChange={this.change}>
                {arrayOfOptions}
            </select>
        </div>)
    }
}


class DatePicker extends React.Component {
    render() {
        return(<div>
            <h3>{this.props.data.context.title}</h3>
            <input type="text" id={this.props.data.id} className="form-control has-date-picker" />
        </div>)
    }
}

class Select2Filter extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            open: [],
            value: []
        }
    }

    toggleOpen() {
        this.setOpen(!this.state.open);
    }

    setOpen(open) {
        this.setState({open});
        openCloseStore.setFilterState(this.props.name, open);
    }

    getCheckedValues = () => {
        var values = this.props.value;
        return _.isArray(values) ? values : []
    }

    isSelected = (value) => {
        let selectedValues = this.getCheckedValues();
        return selectedValues.indexOf(value) >= 0
    }

    getOnChangeHandler = (e) => {
        this.setState({value: $(e.currentTarget).val()},() => {this.props.action(this.props.data.id, this.state.value || [])})
    }

    render() {
        let {open} = this.state;

        let select2events = [
            ['change.react-select2-wrapper', 'onChange'],
            ['select2:open.react-select2-wrapper', 'onOpen'],
            ['select2:close.react-select2-wrapper', 'onClose'],
            ['select2:select.react-select2-wrapper', 'onSelect'],
            ['select2:unselect.react-select2-wrapper', 'onUnselect'],
        ];

        let triangleStyle = {};
        if (!open) {
            triangleStyle.transform = 'rotate(-90deg)'
        }

        return (<div>
            <h3>{this.props.data.context.title}</h3>

            <div className="filter-category-selections" ref="selections">
                <Select2Component
                    multiple
                    data={this.props.data.context.options}
                    value={this.state.value}
                    events={select2events}
                    onChange={this.getOnChangeHandler}
                    isSelected={this.isSelected}
                    options={
                        {
                            placeholder: "Start typing",
                            width: '100%',

                            allowClear: true
                        }
                    }
                />
            </div>
        </div>)
    }
}

class CheckboxFilter extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            options: []
        }
    }

    change = (e) => {
        const options = [...this.state.options];
        let index;

        if (e.target.checked) {
          options.push(e.target.value)
        } else {
          index = options.indexOf(e.target.value)
          options.splice(index, 1)
        }

        this.setState({ options: options })
        this.props.action(this.props.data.id, options);
    }

    render() {
        var arrayOfOptions = this.props.data.context.options.map(obj => {
            return(<div className="checkbox-field" key={obj[0]}>
                <input id={obj[0]} type="checkbox" value={obj[0]} name={this.props.data.id} onChange={this.change} />
                <label htmlFor={obj[0]}>{obj[1]}</label>
            </div>)
        });
        return (
            <div>
                <h3>{this.props.data.context.title}</h3>
                {arrayOfOptions}
            </div>
        )
    }
}
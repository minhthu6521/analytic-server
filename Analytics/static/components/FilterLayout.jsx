class FilterLayout extends React.Component {
    constructor(props) {
        super(props);
    }

    mapFilter = (obj) => {
        if (obj.type === "dropdown_widget") {
            return (<DropdownFilter data={obj} key={obj.id} action={this.props.setFilter} />)
        } else if (obj.type === "select2_widget" ) {
            return (<Select2Filter data={obj} key={obj.id} action={this.props.setFilter}/>)
        } else if (obj.type === "checkbox_widget") {
            return (<CheckboxFilter data={obj} key={obj.id} action={this.props.setFilter}/>)
        }
    }

    render() {
        var arrayOfGeneralFilters = this.props.plan["general"]["items"].map(obj => {
            return this.mapFilter(obj);

        });
        var arrayOfSpecificFilters = this.props.plan["specific"]["items"].map(obj => {
            return this.mapFilter(obj);

        });
        return (<div className="filter-container">
                <h2>Filters</h2>
                {arrayOfGeneralFilters}
                {arrayOfSpecificFilters}
                </div>)
    }
}


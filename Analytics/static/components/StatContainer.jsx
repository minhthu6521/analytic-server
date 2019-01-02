const plan = JSON.parse(document.getElementById("search_plan").innerText);
const api = $("#fetch-api").data("fetch_api");

class StatContainer extends React.Component {
    constructor() {
        super();
        this.state = {
            filter: {},
            data: []
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if(!_.isEqual(this.state.filter, prevState.filter)) {
            this.updateData();
        }
    }

    updateData = () => {
        $.ajax({
            type: 'GET',
            url: this.props.api,
            data: {data: JSON.stringify(this.state.filter || {})},
            success: (data) => {
                this.setState({
                    data: data
                })
            }
        });
    }

    componentDidMount() {
        this.updateData();
    }

    setFilter = (id, value) => {
        this.setState({
            filter: {
                ...this.state.filter,
                [id]: value
            }
        })
    }

    render() {
        return (
        <div>
            <FilterLayout plan={this.props.plan}  setFilter={this.setFilter}/>
            <GraphLayout data={this.state.data}/>
        </div>
        )
    }
}

ReactDOM.render(<StatContainer plan={plan} api={api}/>, document.getElementById("stat_container"));
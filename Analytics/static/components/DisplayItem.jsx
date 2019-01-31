class DisplayItem extends React.Component {

    mapItem = (obj) => {
        if (obj["display_type"] === "line_chart") {
            return (<LineChart data={obj["data"]} id={obj.id} key={obj.id}/>)
        }
        else if (obj["display_type"] == "text") {
            return (<TextField data={obj["data"]} id={obj.id} key={obj.id}/>)
        }
        else if (obj["display_type"] == "pie_chart") {
            return(<PieChart data={obj["data"]} id={obj.id} key={obj.id}/>)
        }
        else if (obj["display_type"] == "bar_chart") {
            return(<BarChart data={obj["data"]} id={obj.id} key={obj.id}/>)
        }
    }


    render() {
        var arrayOfItems = this.props.data["items"].map(obj => {
            return this.mapItem(obj);

        });
        return (<div>
            <h4>{this.props.data.title}</h4>
            {arrayOfItems}
        </div>)
    }
}


class LineChart extends React.Component {

    updateChart = () => {
        var chart_data = {
            type: "line",
            data: this.props.data,
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
        var ctx = document.getElementById(this.props.id).getContext('2d');
        var myChart = new Chart(ctx, chart_data);
    }


    componentDidUpdate(prevProps) {
        if (!_.isEqual(this.props.data, prevProps.data)) {
            this.updateChart();
        }
    }

    componentDidMount() {
        this.updateChart();
    }

    render() {
        return (
            <canvas style={{maxHeight: "400px", maxWidth: "800px"}} id={this.props.id}></canvas>)
    }
}

class BarChart extends React.Component {

    updateChart = () => {
        var chart_data = {
            type: "bar",
            data: this.props.data,
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
        var ctx = document.getElementById(this.props.id).getContext('2d');
        var myChart = new Chart(ctx, chart_data);
    }


    componentDidUpdate(prevProps) {
        if (!_.isEqual(this.props.data, prevProps.data)) {
            this.updateChart();
        }
    }

    componentDidMount() {
        this.updateChart();
    }

    render() {
        return (
            <canvas style={{maxHeight: "400px", maxWidth: "800px"}} id={this.props.id}></canvas>)
    }
}

class TextField extends React.Component {
    render() {
        const all_labels = this.props.data.datasets.map(obj => {
            return (
                <div>
                    <label className="stat-display text-field text-field-label">{obj["label"]}</label>
                    <span className="stat-display text-field text-field-data">{obj["data"][0]}</span>
                </div>
            )
        })
        return (
            <div>{all_labels}</div>
        )
    }
}

class PieChart extends React.Component {

    updateChart = () => {
        var chart_data = {
            type: "pie",
            data: this.props.data
        };
        var ctx = document.getElementById(this.props.id).getContext('2d');
        var myChart = new Chart(ctx, chart_data);
    }

    canUpdate = () => {
        return !this.props.data.datasets[0].data.every(e => {return e == 0})
    }

    componentDidUpdate(prevProps) {
        if (!_.isEqual(this.props.data, prevProps.data)) {
            if (this.canUpdate()) {
                this.updateChart();
            }
        }
    }

    componentDidMount() {
        if (this.canUpdate()) {
                this.updateChart();
            }
    }

    render() {
        if(!this.canUpdate()) {
         return (
             <div>Not enough data</div>
         )
        } else {
            return (
                <canvas style={{maxHeight: "400px", maxWidth: "800px"}} id={this.props.id}></canvas>)
        }
    }
}
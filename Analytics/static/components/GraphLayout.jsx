class GraphLayout extends React.Component {
    constructor() {
        super();
        this.state = {
            data: []
        }
    }

    componentDidMount() {
        fetch('/api/dashboard')
          .then((response) => {
            return response.json();
          })
          .then((myJson) => {
            this.setState({data: myJson});
          });


    }

    render() {
        var arrayOfCanvas = this.state.data.map(obj => {
            return (<GraphTemplate data={obj} key={obj.id} />)
        })
        return (<div>{arrayOfCanvas}</div>)
    }
}

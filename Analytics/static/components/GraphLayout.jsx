class GraphLayout extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        var arrayOfCanvas = this.props.data.map(obj => {
            return (<GraphTemplate data={obj} key={obj.id} />)
        });
        return (<div>{arrayOfCanvas}</div>)
    }
}

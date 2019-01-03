class DisplayLayout extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        var arrayOfCanvas = this.props.data.map(obj => {
            return (<DisplayItem data={obj} key={obj.id} />)
        });
        return (<div>{arrayOfCanvas}</div>)
    }
}

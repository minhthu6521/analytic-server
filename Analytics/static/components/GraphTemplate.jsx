class GraphTemplate extends React.Component {
    componentDidMount() {
         var ctx = document.getElementById(this.props.data.id).getContext('2d');;
         var myChart = new Chart(ctx, this.props.data);
    }

    render()  {
        return(<canvas key={this.props.data.id} id={this.props.data.id}></canvas>)
    }
}

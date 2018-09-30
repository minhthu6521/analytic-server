
const App = () => {
    const changeTimeRange = () => {
        console.log(timerange.value)
    }
    return(
        <div>
          <GraphLayout />
          <select onChange={changeTimeRange} id="timerange">
            <option value="7">7 days</option>
            <option value="30">1 month</option>
            <option value="90">3 months</option>
          </select>
        </div>)
    };

ReactDOM.render(<App />, document.getElementById("container"));

import React from 'react';
import $ from 'jquery';

class PatientTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      appointments: [],
    }
  }

  componentDidMount() {
   $.ajax({
      method: 'GET',
      url: 'api/getAppointments',
      // data: data,
    }).done((data) => {
      data = JSON.parse(data)
      this.setState({appointments: data})
    })
  }

  render() {
    return(
      <table className="striped">
    <thead>
      <tr>
        <th data-field="id">Name</th>
        <th data-field="name">Scheduled Time</th>
        <th data-field="price">Waiting Time</th>
    </tr>
    </thead>
    <tbody>
      {this.state.appointments.map(function(value, index) {
        return (
          <tr>
            <td key={index + .1}>{value.first_name + ' ' + value.last_name}</td>
            <td key={index + .2}>{value.scheduled_time}</td>
            <td key={index + .3}></td>
          </tr>
          )
      })}
    </tbody>
  </table>
    );
  }
}

export default PatientTable;
      // <tr>
      //   <td>Alan</td>
      //   <td>Jellybean</td>
      //   <td>$3.76</td>
      // </tr>
      // <tr>
      //   <td>Alan</td>
      //   <td>Jellybean</td>
      //   <td>$3.76</td>
      // </tr>
      // <tr>
      //   <td>Jonathan</td>
      //   <td>Lollipop</td>
      //   <td>$7.00</td>
      // </tr>
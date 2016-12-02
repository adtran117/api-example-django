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
      console.log(data)

      this.setState({appointments: data})
    })
  }

  getWaitingTime(time, readyTime) {    
    if(!time) {
      return 'Not checked in'
    }
    console.log(readyTime);
    if(readyTime) {
      var today = Date.parse(readyTime + 'UTC');
      console.log(today)
    } else {
      var today = new Date();
    }

    var checkin= Date.parse(time + 'UTC');
    var diffMs = (today-checkin);
    var diffHrs = Math.floor((diffMs % 86400000) / 3600000); // hours
    var diffMins = Math.floor(((diffMs % 86400000) % 3600000) / 60000); // minutes
    // var diffSecs = ((((diffMs  % 86400000) % 3600000) / 60000) / 1000);
    // console.log(time)
    // var start = Date.parse(time);
    // var end = new Date().getTime();
    // var diffMs = new Date(end - start);
    // var diffMins = diffMs.getMinutes();
    // var diffSecs = diffMs.getSeconds();
    return diffHrs + ' hrs ' + diffMins + ' mins '  ;
  }

  stopTimer(appointmentId){
    let data = {
      appointment_id: appointmentId
    }
    $.ajax({
      method: 'GET',
      url: 'api/stopTimer',
      data: data,
    }).done((data) => {
      console.log('here')
      // db marked appointment timer to stop

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
        <th data-field="ready">Ready</th>
    </tr>
    </thead>
    <tbody>
      {this.state.appointments.map(function(value, index) {
        return (
          <tr>
            <td key={index + .1}>{value.first_name + ' ' + value.last_name}</td>
            <td key={index + .2}>{new Date(Date.parse(value.scheduled_time)).toString()}</td>
            <td key={index + .3}>{this.getWaitingTime(value.time_checkedin, value.time_ready)}</td>
            {value.time_checkedin === undefined || value.time_ready ? <td key ={index + .4}></td> : <td>
              <a key = {index + .4} onClick={this.stopTimer.bind(this, value.id)} className="waves-effect waves-light btn">Ready</a></td> }
          </tr>
          )
      }.bind(this))}
    </tbody>
  </table>
    );
  }
}

export default PatientTable;

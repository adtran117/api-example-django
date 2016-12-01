import React from 'react';
import { browserHistory } from 'react-router';

import Forms from  '../components/Forms'
import DemographicForms from  '../components/DemographicForms'
import $ from 'jquery';


class FormContainer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      patientExists: false,
      currentPatientId: null,
    }
    console.log(props)
  }


  handleSubmit(event) {
    if (this.state.patientExists === false) {
      let firstName = document.getElementById('first_name').value;
      let lastName = document.getElementById('last_name').value;
      $.ajax({
        method: 'GET',
        url: 'api/validateCheckInUser',
        data: {first_name: firstName, last_name: lastName}
      }).done((data) => {
        data = JSON.parse(data);
        console.log(data);
        if(data !== false) {
          this.setState({patientExists: true, currentPatientId: data});
        }
      });
    }

    else {
      let data = {
        'csrfmiddlewaretoken': "{{ csrf_token }}", 
        city: document.getElementById('city').value,
        zip_code: document.getElementById('zip_code').value,
        home_phone: document.getElementById('homephone').value,
        address: document.getElementById('streetaddress').value,
        patient_id: this.state.currentPatientId,
      }

      $.ajax({
        method: 'GET',
        url: 'api/updatePatientDemo',
        data: data,
      }).done((data) => {
        if (data === '204') {
          console.log('success!')
          this.props.completedCheckIn();
        }
      })

      
    }
  }

  render() {
    return(
       <div className="row">
        <div className="col s12 m12">
          <div className="card blue-grey darken-1">
            <div className="card-content white-text">
              <span className="card-title">Check In</span>
              {this.state.patientExists ? <DemographicForms /> : <Forms />}
            </div>
            <div className="card-action">
              <a href="#" className="submitBtn" onClick={this.handleSubmit.bind(this)}>Submit</a>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default FormContainer

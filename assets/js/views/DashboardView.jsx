import React from 'react';
import PatientTable from '../components/PatientTable'

class DashboardView extends React.Component {
  render() {
    return(
      <div>
        <div className='container'>
          <h1 className='header center light-green-text'>Today's Appointments</h1>
          <PatientTable />
        </div>
      </div>
    );
  }
}

export default DashboardView;

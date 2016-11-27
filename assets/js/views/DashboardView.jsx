import React from 'react';
import PatientTable from '../components/PatientTable'

class DashboardView extends React.Component {
  render() {
    return(
      <div>
        <h1> No Birthdays today</h1>
        <PatientTable />
      </div>
    );
  }
}

export default DashboardView;

import React from 'react';

let DefaultCheckInView = (props) => (
  <div className="section no-pad-bot" id="index-banner">
    <div className="container">
      <br></br>
      <h1 className="header center light-blue-text">Check In Here</h1>
      <div className="row center">
        <a onClick={props.nextBtn} className="btn-large waves-effect waves-light light-blue">Next</a>
      </div>
      <br></br>
    </div>
  </div>
);

export default DefaultCheckInView;



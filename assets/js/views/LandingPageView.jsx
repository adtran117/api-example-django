import React from 'react';

class LandingPageView extends React.Component {
  render() {
    return(
      <div className="section no-pad-bot" id="index-banner">
    <div className="container">
      <br></br>
      <h1 className="header center light-blue-text">Birthday App</h1>
      <div className="row center">
        <h5 className="header col s12 light">Say 'Happy Birthday!' to your patients</h5>
      </div>
      <div className="row center">
        <a href="/api/login" id="download-button" className="btn-large waves-effect waves-light light-blue">Login</a>
      </div>
      <br></br>

    </div>
  </div>

    );
  }
}

export default LandingPageView;



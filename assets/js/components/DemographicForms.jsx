import React from 'react';

class Forms extends React.Component {
  render() {
    return(
        <div className="row">
        <form className="col s12">
          <div className="row">
            <div className="input-field col s12">
              <input id="homephone" type="text" className="validate"></input>
              <label htmlFor="homephone">Home Phone</label>
            </div>
          </div>
          <div className="row">
            <div className="input-field col s12">
              <textarea id="streetaddress" className="materialize-textarea"></textarea>
              <label htmlFor="streetaddress">Street Address</label>
            </div>
          </div>
          <div className="row">
            <div className="input-field col s12">
              <input id="city" type="text" className="validate"></input>
              <label htmlFor="city">City</label>
            </div>
          </div>
          <div className="row">
            <div className="input-field col s12">
              <input id="zip_code" type="text" className="validate"></input>
              <label htmlFor="zip_code">Zip Code</label>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default Forms
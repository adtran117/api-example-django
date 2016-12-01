import React from 'react';

class Forms extends React.Component {
  render() {
    return(
        <div className="row">
        <form className="col s12">
          <div className="row">
            <div className="input-field col s12">
              <input id="first_name" type="text" className="validate"></input>
              <label htmlFor="first_name">First Name</label>
            </div>
          </div>
          <div className="row">
            <div className="input-field col s12">
              <input id="last_name" type="text" className="validate"></input>
              <label htmlFor="last_name">Last Name</label>
            </div>
          </div>
        </form>
      </div>
    );
  }
}

export default Forms
import React from 'react';
import FormContainer from '../components/FormContainer'
import DefaultCheckInView from '../components/DefaultCheckInView'

class CheckInView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      pressedCheckIn: false,
      completedCheckIn: false,
    }
  }

  nextBtn() {
    this.setState({pressedCheckIn: true});
  }

  completedCheckIn() {
    this.setState({completedCheckIn: true, pressedCheckIn:false});
    setTimeout(function(){
    this.setState({completedCheckIn: false});
    }.bind(this), 5000)
  }

  render() {
    return(

      <div className="container">
        {this.state.completedCheckIn === true ? <h1 className="header center light-green-text">Success!</h1> :

        (this.state.pressedCheckIn ? <FormContainer completedCheckIn={this.completedCheckIn.bind(this)}/> : 
          <DefaultCheckInView nextBtn={this.nextBtn.bind(this)} completedCheckIn={this.state.completedCheckIn}/>)
        }
      </div>
    );
  }
}

export default CheckInView

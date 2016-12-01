import React from 'react';
import NavBar from './components/NavBar'

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: null,
    }
  }

    componentDidMount () {
        $.ajax({
          method: 'GET',
          url: 'api/getUserInfo',
        }).done((data) => {
          console.log(data);
          data = JSON.parse(data);
          this.setState({username: data});
        })
    }

  render() {
    return(
      <div>
        <div>
          <NavBar username={this.state.username}/>
            {this.props.children}
        </div>
      </div>
    )
  }
}

export default Main;